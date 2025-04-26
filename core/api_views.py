from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import MediaContent, Comment, Rating
from .serializers import (
    MediaContentSerializer, 
    MediaContentListSerializer, 
    CommentSerializer, 
    RatingSerializer
)

class IsCreator(permissions.BasePermission):
    """
    Custom permission to only allow creators to upload content.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'is_creator') and request.user.is_creator

class IsConsumer(permissions.BasePermission):
    """
    Custom permission to only allow consumers to interact with content.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'is_consumer') and request.user.is_consumer

class MediaPagination(PageNumberPagination):
    """
    Pagination for media content lists (10 items per page).
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class MediaContentListCreateView(generics.ListCreateAPIView):
    """
    API view to list all media content or create a new one.
    """
    pagination_class = MediaPagination
    queryset = MediaContent.objects.filter(is_active=True).order_by('-upload_date')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MediaContentSerializer
        return MediaContentListSerializer
    
    def get_permissions(self):
        """
        List is available to all, create only to creators.
        """
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCreator()]
        return [permissions.AllowAny()]
    
    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class MediaContentDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a specific media content item.
    """
    queryset = MediaContent.objects.filter(is_active=True)
    serializer_class = MediaContentSerializer
    permission_classes = [permissions.AllowAny]

class CommentCreateView(generics.CreateAPIView):
    """
    API view to create a new comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsumer]
    
    def create(self, request, *args, **kwargs):
        # Get the media ID from the request data
        media_id = request.data.get('media_id')
        if not media_id:
            return Response(
                {'error': 'media_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the media exists and is active
        try:
            media = MediaContent.objects.get(pk=media_id, is_active=True)
        except MediaContent.DoesNotExist:
            return Response(
                {'error': 'Media not found or inactive'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create the serializer with the media_id in context
        serializer = self.get_serializer(
            data=request.data, 
            context={'request': request, 'media_id': media_id}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

class RatingCreateView(generics.CreateAPIView):
    """
    API view to create or update a rating.
    """
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated, IsConsumer]
    
    def create(self, request, *args, **kwargs):
        # Get the media ID from the request data
        media_id = request.data.get('media_id')
        if not media_id:
            return Response(
                {'error': 'media_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the media exists and is active
        try:
            media = MediaContent.objects.get(pk=media_id, is_active=True)
        except MediaContent.DoesNotExist:
            return Response(
                {'error': 'Media not found or inactive'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create the serializer with the media_id in context
        serializer = self.get_serializer(
            data=request.data, 
            context={'request': request, 'media_id': media_id}
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        ) 