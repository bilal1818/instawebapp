from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('media/', views.media_list, name='media_list'),
    path('search/', views.media_search, name='media_search'),
    path('media/<int:pk>/', views.media_detail, name='media_detail'),
    path('media/<int:pk>/edit/', views.media_update, name='media_update'),
    path('media/<int:pk>/delete/', views.media_delete, name='media_delete'),
    path('upload/', views.upload_media, name='upload_media'),
    path('media/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('media/<int:pk>/rate/', views.add_rating, name='add_rating'),
    path('media/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('media/<int:pk>/save/', views.toggle_save, name='toggle_save'),
    path('saved-posts/', views.saved_posts, name='saved_posts'),
    path('api-test/', views.api_test, name='api_test'),
] 