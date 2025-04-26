from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, F
from users.views import creator_required
from .models import MediaContent, Comment, Rating, Like, SavedPost
from .forms import MediaContentForm, CommentForm, RatingForm

# Create your views here.

def home(request):
    """
    Home page view to display the landing page of the application.
    """
    # Get trending media (most viewed/liked in the last 30 days)
    trending_media = MediaContent.objects.filter(is_active=True).annotate(
        popularity=Count('likes') + F('views')
    ).order_by('-popularity')[:4]
    
    # Get the latest media uploads
    latest_media = MediaContent.objects.filter(is_active=True).order_by('-upload_date')[:4]
    
    return render(request, 'core/home.html', {
        'trending_media': trending_media,
        'latest_media': latest_media
    })

def media_list(request):
    """
    View to display a paginated list of all active media content
    """
    media_list = MediaContent.objects.filter(is_active=True).order_by('-upload_date')
    paginator = Paginator(media_list, 10)  # Show 10 items per page
    
    page_number = request.GET.get('page', 1)
    media = paginator.get_page(page_number)
    
    return render(request, 'core/list.html', {'media': media})

def media_search(request):
    """
    View to search for media content by keywords in title, caption, or location
    """
    query = request.GET.get('query', '')
    results = []
    
    if query:
        results = MediaContent.objects.filter(
            Q(title__icontains=query) | 
            Q(caption__icontains=query) | 
            Q(location__icontains=query),
            is_active=True
        ).order_by('-upload_date')
    
    paginator = Paginator(results, 10)  # Show 10 items per page
    page_number = request.GET.get('page', 1)
    results_page = paginator.get_page(page_number)
    
    return render(request, 'core/search.html', {
        'query': query,
        'results': results_page
    })

def media_detail(request, pk):
    """
    View to display the details of a specific media item, with comments and ratings
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    comments = media.comments.all().order_by('-created_at')
    
    # Calculate average rating
    avg_rating = media.ratings.aggregate(Avg('score'))['score__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0
    
    # Get related media based on category or creator
    related_media = MediaContent.objects.filter(
        Q(category=media.category) | Q(creator=media.creator),
        is_active=True
    ).exclude(id=media.id).distinct().order_by('-upload_date')[:6]
    
    # Show comment and rating forms only to consumers
    comment_form = None
    rating_form = None
    user_rating = None
    has_liked = False
    has_saved = False
    
    if request.user.is_authenticated and hasattr(request.user, 'is_consumer') and request.user.is_consumer:
        comment_form = CommentForm()
        rating_form = RatingForm()
        
        # Check if user has already rated this media
        try:
            user_rating = Rating.objects.get(user=request.user, media=media)
            rating_form = RatingForm(instance=user_rating)
        except Rating.DoesNotExist:
            pass
        
        # Check if user has liked this media
        has_liked = Like.objects.filter(user=request.user, media=media).exists()
        
        # Check if user has saved this media
        has_saved = SavedPost.objects.filter(user=request.user, media=media).exists()
    
    # Increment view count
    media.views += 1
    media.save()
    
    return render(request, 'core/media_detail.html', {
        'object': media,
        'comments': comments,
        'avg_rating': avg_rating,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
        'has_liked': has_liked,
        'has_saved': has_saved,
        'related_media': related_media
    })

@login_required
@creator_required
def upload_media(request):
    """
    View for creators to upload new media content
    """
    if request.method == 'POST':
        form = MediaContentForm(request.POST, request.FILES, creator=request.user)
        if form.is_valid():
            media = form.save()
            messages.success(request, f"'{media.title}' was uploaded successfully!")
            return redirect('core:media_detail', pk=media.pk)
    else:
        form = MediaContentForm(creator=request.user)
    
    return render(request, 'core/upload.html', {'form': form})

@login_required
def add_comment(request, pk):
    """
    View for consumers to add comments to media content
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    
    # Only consumers can comment
    if not hasattr(request.user, 'is_consumer') or not request.user.is_consumer:
        messages.error(request, "Only consumers can add comments.")
        return redirect('core:media_detail', pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.media = media
            comment.save()
            messages.success(request, "Your comment was added successfully!")
    
    return redirect('core:media_detail', pk=pk)

@login_required
def add_rating(request, pk):
    """
    View for consumers to rate media content
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    
    # Only consumers can rate
    if not hasattr(request.user, 'is_consumer') or not request.user.is_consumer:
        messages.error(request, "Only consumers can rate content.")
        return redirect('core:media_detail', pk=pk)
    
    if request.method == 'POST':
        # Check if user has already rated this media
        try:
            rating = Rating.objects.get(user=request.user, media=media)
            form = RatingForm(request.POST, instance=rating)
        except Rating.DoesNotExist:
            form = RatingForm(request.POST)
        
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.media = media
            rating.save()
            messages.success(request, "Your rating was saved successfully!")
    
    return redirect('core:media_detail', pk=pk)

def api_test(request):
    """
    View to render the API test page.
    """
    return render(request, 'core/api_test.html')

@login_required
def toggle_like(request, pk):
    """
    View for consumers to like/unlike media content
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    
    # Only consumers can like
    if not hasattr(request.user, 'is_consumer') or not request.user.is_consumer:
        messages.error(request, "Only consumers can like content.")
        return redirect('core:media_detail', pk=pk)
    
    like, created = Like.objects.get_or_create(user=request.user, media=media)
    
    if not created:
        # If like already existed, remove it (unlike)
        like.delete()
        messages.success(request, "Post unliked successfully!")
    else:
        messages.success(request, "Post liked successfully!")
    
    return redirect('core:media_detail', pk=pk)

@login_required
def toggle_save(request, pk):
    """
    View for consumers to save/unsave media content
    """
    media = get_object_or_404(MediaContent, pk=pk, is_active=True)
    
    # Only consumers can save posts
    if not hasattr(request.user, 'is_consumer') or not request.user.is_consumer:
        messages.error(request, "Only consumers can save posts.")
        return redirect('core:media_detail', pk=pk)
    
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, media=media)
    
    if not created:
        # If post was already saved, remove it (unsave)
        saved_post.delete()
        messages.success(request, "Post removed from saved items!")
    else:
        messages.success(request, "Post saved successfully!")
    
    return redirect('core:media_detail', pk=pk)

@login_required
def saved_posts(request):
    """
    View to display all saved posts by the current user
    """
    if not hasattr(request.user, 'is_consumer') or not request.user.is_consumer:
        messages.error(request, "Only consumers can view saved posts.")
        return redirect('core:home')
    
    saved_posts = SavedPost.objects.filter(user=request.user).select_related('media')
    paginator = Paginator(saved_posts, 10)  # Show 10 items per page
    
    page_number = request.GET.get('page', 1)
    saved_posts_page = paginator.get_page(page_number)
    
    return render(request, 'core/saved_posts.html', {'saved_posts': saved_posts_page})

@login_required
@creator_required
def media_update(request, pk):
    """
    View for creators to update their media content
    """
    media = get_object_or_404(MediaContent, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        form = MediaContentForm(request.POST, request.FILES, instance=media, creator=request.user)
        if form.is_valid():
            media = form.save()
            messages.success(request, f"'{media.title}' was updated successfully!")
            return redirect('core:media_detail', pk=media.pk)
    else:
        form = MediaContentForm(instance=media, creator=request.user)
    
    return render(request, 'core/upload.html', {
        'form': form,
        'is_update': True,
        'media': media
    })

@login_required
@creator_required
def media_delete(request, pk):
    """
    View for creators to delete their media content
    """
    media = get_object_or_404(MediaContent, pk=pk, creator=request.user)
    
    if request.method == 'POST':
        title = media.title
        media.delete()
        messages.success(request, f"'{title}' was deleted successfully!")
        return redirect('core:media_list')
    
    return render(request, 'core/media_delete.html', {'media': media})
