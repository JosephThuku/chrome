# video_api/urls.py
from django.urls import path
from .views import video_list, video_detail

urlpatterns = [
    path('videos/', video_list, name='video-list'),
    path('videos/<int:pk>/', video_detail, name='video-detail'),
]
