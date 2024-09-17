from django.urls import path
from . import views

urlpatterns = [
    # URL for video upload
    path('upload/', views.upload_video, name='upload_video'),
    
    # URL for listing all uploaded videos
    path('videos/', views.video_list, name='video_list'),
    
    # URL for viewing a specific video and its subtitles
    path('videos/<int:video_id>/', views.video_detail, name='video_detail'),
    
    # URL for searching subtitles within a video
    path('search/', views.search_subtitle, name='search_subtitle'),
    path('search_subtitle/', views.search_subtitle, name='search_subtitle'),
]
