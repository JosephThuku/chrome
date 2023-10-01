from django.db import models

class Video(models.Model):
    #title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    unique_filename = models.CharField(max_length=255)  # Unique filename for the video
    recording_started = models.DateTimeField(null=True, blank=True)  # Timestamp when recording started
    recording_completed = models.DateTimeField(null=True, blank=True)  # Timestamp when recording completed
    transcription = models.OneToOneField('Transcription', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.unique_filename

# video_api/models.py
class Transcription(models.Model):
    text = models.TextField()  # The transcribed text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the transcription was created

    def __str__(self):
        return f"Transcription for Video ({self.created_at})"
