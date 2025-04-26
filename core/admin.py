from django.contrib import admin
from .models import MediaContent, Comment, Rating, Like, SavedPost

@admin.register(MediaContent)
class MediaContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'upload_date', 'is_active')
    list_filter = ('is_active', 'upload_date')
    search_fields = ('title', 'caption', 'location')
    date_hierarchy = 'upload_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'media', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'media__title')
    date_hierarchy = 'created_at'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('score', 'user', 'media', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user__username', 'media__title')
    date_hierarchy = 'created_at'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'media__title')
    date_hierarchy = 'created_at'

@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'media', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'media__title')
    date_hierarchy = 'saved_at'
