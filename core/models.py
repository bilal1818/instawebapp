from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.conf import settings

# Create your models here.

class MediaContent(models.Model):
    """
    Model for storing uploaded media content (videos and photos)
    """
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'creator'},
        related_name='media_content'
    )
    file = models.FileField(upload_to='media_content/')
    title = models.CharField(max_length=100)
    caption = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    people_present = models.TextField(max_length=200, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-upload_date']

class Comment(models.Model):
    """
    Model for storing user comments on media content
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'consumer'},
        related_name='comments'
    )
    media = models.ForeignKey(
        MediaContent,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        max_length=300,
        validators=[MaxLengthValidator(300)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.media.title}"
    
    class Meta:
        ordering = ['-created_at']

class Rating(models.Model):
    """
    Model for storing user ratings on media content
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'consumer'},
        related_name='ratings'
    )
    media = models.ForeignKey(
        MediaContent,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rating of {self.score} by {self.user.username} on {self.media.title}"
    
    class Meta:
        ordering = ['-created_at']
        # Ensure one rating per user per media item
        unique_together = ['user', 'media']

class Like(models.Model):
    """
    Model for storing user likes on media content
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'consumer'},
        related_name='likes'
    )
    media = models.ForeignKey(
        MediaContent,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Like by {self.user.username} on {self.media.title}"
    
    class Meta:
        ordering = ['-created_at']
        # Ensure one like per user per media item
        unique_together = ['user', 'media']

class SavedPost(models.Model):
    """
    Model for storing saved posts by consumers
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'consumer'},
        related_name='saved_posts'
    )
    media = models.ForeignKey(
        MediaContent,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Saved post {self.media.title} by {self.user.username}"
    
    class Meta:
        ordering = ['-saved_at']
        # Ensure one save per user per media item
        unique_together = ['user', 'media']
