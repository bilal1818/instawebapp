from django.urls import path
from . import api_views

app_name = 'api'

urlpatterns = [
    path('media/', api_views.MediaContentListCreateView.as_view(), name='media-list-create'),
    path('media/<int:pk>/', api_views.MediaContentDetailView.as_view(), name='media-detail'),
    path('comments/', api_views.CommentCreateView.as_view(), name='comment-create'),
    path('ratings/', api_views.RatingCreateView.as_view(), name='rating-create'),
] 