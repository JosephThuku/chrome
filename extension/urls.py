# video_api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('videos/', views.VideoUpload.as_view(), name='video-upload'),
    path('videos/<int:pk>/', views.video_detail, name='video-detail'),
    path('upload/', views.upload_and_create_video, name='upload-and-create-video'),  # New endpoint for combined upload and creation
]
