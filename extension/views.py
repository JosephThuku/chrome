# video_api/views.py
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VideoSerializer
from .models import Video
import base64
import uuid
import time
# Set your OpenAI API key
import openai
openai.api_key = ("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")


def generate_unique_filename():
    random_string = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    return f"{random_string}_{timestamp}"

@api_view(['GET', 'POST'])
def video_list(request):
    if request.method == 'GET':
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        video_chunk = request.data.get('video_chunk')

        if video_chunk:
            unique_filename = generate_unique_filename()
            file_path = os.path.join(settings.MEDIA_ROOT, f'{unique_filename}.mp4')

            binary_data = base64.b64decode(video_chunk)

            with open(file_path, 'wb+') as destination:
                destination.write(binary_data)

            # You can also save the file path to your database here
            # Create a Video object and associate it with the file path

            return Response({'message': 'Video chunk saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Video chunk not saved'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def video_detail(request, pk):
    try:
        video = Video.objects.get(pk=pk)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = VideoSerializer(video)
    
    # Generate transcription for the video
    video_path = os.path.join(settings.MEDIA_ROOT, f'{video.unique_filename}.mp4')
    transcription = generate_transcription(video_path)

    # Create a response with the video data and transcription
    response_data = {
        'video_data': serializer.data,
        'transcription': transcription,
    }

    return Response(response_data)


def generate_transcription(video_path):
    # Define the parameters for the Whisper API call
    params = {
        "audio": video_path,
        "engine": "davinci",
        "format": "text",
    }

    # Make the API call
    response = openai.Transcriber.create(**params)

    # Extract and return the transcription
    transcription = response['text']
    return transcription
