from django.db import models

class Video(models.Model):
    #title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    Title = models.CharField(max_length=255)  # Unique filename for the video

    def __str__(self):
        return self.Title

# video_api/models.py
class Transcription(models.Model):
    text = models.TextField()  # The transcribed text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the transcription was created
    video = models.ForeignKey(Video, on_delete=models.CASCADE)  # The video associated with the transcription

    def __str__(self):
        return f"Transcription for Video ({self.created_at})"
