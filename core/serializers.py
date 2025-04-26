from rest_framework import serializers
from .models import MediaContent, Comment, Rating, Like, SavedPost
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model (simplified)"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'role']
        read_only_fields = ['id', 'username', 'role']

class RatingSerializer(serializers.ModelSerializer):
    """Serializer for the Rating model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rating
        fields = ['id', 'user', 'score', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """Create and return a new rating"""
        user = self.context['request'].user
        media_id = self.context['media_id']
        
        # Check if the user already rated this media
        try:
            rating = Rating.objects.get(user=user, media_id=media_id)
            rating.score = validated_data['score']
            rating.save()
            return rating
        except Rating.DoesNotExist:
            return Rating.objects.create(
                user=user,
                media_id=media_id,
                **validated_data
            )

class LikeSerializer(serializers.ModelSerializer):
    """Serializer for the Like model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """Create a new like or return None if it already exists"""
        user = self.context['request'].user
        media_id = self.context['media_id']
        
        like, created = Like.objects.get_or_create(
            user=user,
            media_id=media_id
        )
        
        # If like already existed, delete it (unlike)
        if not created:
            like.delete()
            return None
        
        return like

class SavedPostSerializer(serializers.ModelSerializer):
    """Serializer for the SavedPost model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = SavedPost
        fields = ['id', 'user', 'saved_at']
        read_only_fields = ['id', 'user', 'saved_at']
    
    def create(self, validated_data):
        """Create a new saved post or return None if it already exists"""
        user = self.context['request'].user
        media_id = self.context['media_id']
        
        saved_post, created = SavedPost.objects.get_or_create(
            user=user,
            media_id=media_id
        )
        
        # If saved_post already existed, delete it (unsave)
        if not created:
            saved_post.delete()
            return None
        
        return saved_post

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """Create and return a new comment"""
        user = self.context['request'].user
        media_id = self.context['media_id']
        
        return Comment.objects.create(
            user=user,
            media_id=media_id,
            **validated_data
        )

class MediaContentSerializer(serializers.ModelSerializer):
    """Serializer for the MediaContent model"""
    creator = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    ratings = RatingSerializer(many=True, read_only=True)
    likes = serializers.SerializerMethodField()
    saved_by_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    user_has_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaContent
        fields = [
            'id', 'creator', 'file', 'title', 'caption', 'location', 
            'people_present', 'upload_date', 'is_active', 
            'comments', 'ratings', 'average_rating', 'likes',
            'saved_by_count', 'user_has_liked', 'user_has_saved'
        ]
        read_only_fields = ['id', 'creator', 'upload_date', 'comments', 'ratings']
    
    def get_average_rating(self, obj):
        """Calculate the average rating for a media item"""
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        return sum(rating.score for rating in ratings) / len(ratings)
    
    def get_likes(self, obj):
        """Get the number of likes for a media item"""
        return obj.likes.count()
    
    def get_saved_by_count(self, obj):
        """Get the number of users who have saved this media item"""
        return obj.saved_by.count()
    
    def get_user_has_liked(self, obj):
        """Check if the current user has liked this media item"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, media=obj).exists()
        return False
    
    def get_user_has_saved(self, obj):
        """Check if the current user has saved this media item"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedPost.objects.filter(user=request.user, media=obj).exists()
        return False
    
    def create(self, validated_data):
        """Create and return a new media content item"""
        user = self.context['request'].user
        return MediaContent.objects.create(creator=user, **validated_data)

class MediaContentListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing media content"""
    creator = UserSerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    user_has_saved = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaContent
        fields = [
            'id', 'creator', 'file', 'title', 'upload_date', 
            'is_active', 'average_rating', 'comment_count',
            'likes_count', 'user_has_liked', 'user_has_saved'
        ]
        read_only_fields = ['id', 'creator', 'upload_date']
    
    def get_average_rating(self, obj):
        """Calculate the average rating for a media item"""
        ratings = obj.ratings.all()
        if not ratings:
            return 0
        return sum(rating.score for rating in ratings) / len(ratings)
    
    def get_comment_count(self, obj):
        """Get the comment count for a media item"""
        return obj.comments.count()
        
    def get_likes_count(self, obj):
        """Get the number of likes for a media item"""
        return obj.likes.count()
    
    def get_user_has_liked(self, obj):
        """Check if the current user has liked this media item"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(user=request.user, media=obj).exists()
        return False
    
    def get_user_has_saved(self, obj):
        """Check if the current user has saved this media item"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return SavedPost.objects.filter(user=request.user, media=obj).exists()
        return False 