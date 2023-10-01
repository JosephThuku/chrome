# video_api/urls.py
from django.urls import path
from .views import video_list, video_detail,VedioUpload

urlpatterns = [
    path('chunks/', video_list, name='video-list'),
    path('videos/<int:pk>/', video_detail, name='video-detail'),
    path('videos/', VedioUpload.as_view(), name='video-list')
]
