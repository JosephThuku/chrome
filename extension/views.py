# video_api/views.py
import os
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import VideoSerializer, TranscriptionSerializer
from .models import Video, Transcription
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

@api_view(['POST'])
def upload_and_create_video(request):
    """take a video chunk and save it to the server,
    then generate a transcription for the video"""
    video_chunk = request.data.get('video_chunk')

    if video_chunk:
        try:
            unique_filename = generate_unique_filename()
            file_path = os.path.join(settings.MEDIA_ROOT, f'{unique_filename}.mp4')

            binary_data = base64.b64decode(video_chunk)

            with open(file_path, 'wb+') as destination:
                destination.write(binary_data)

            # You can also save the file path to your database here
            # Create a Video object and associate it with the file path

            # Generate transcription for the video
            transcription = generate_transcription(file_path)

            video = Video.objects.create(title=unique_filename, file_path=file_path)
            transcription = Transcription.objects.create(text=transcription, video=video)

            serializer = VideoSerializer(video)
            serializer2 = TranscriptionSerializer(transcription)

            return Response({'message': 'Video chunk saved successfully', 'video_data': serializer.data, 'transcription': serializer2.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': f'Video chunk not saved - {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Video chunk not saved'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def video_detail(request, pk):
    try:
        video = Video.objects.get(pk=pk)
        #trascrib = Transcription.objects.get(video=video)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = VideoSerializer(video)
    #serializer2 = TranscriptionSerializer(trascrib)

    return Response({'video_data': serializer.data})


class VideoUpload(generics.ListCreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


def generate_transcription(video_path):
    try:
        with open(video_path, 'rb') as audio_file:
            response = openai.Audio.transcribe("whisper-1", engine="davinci", file=audio_file)

        transcription = response['data']['text']  # Extract the transcription text from the response
        return transcription
    except Exception as e:
        # Handle any exceptions or errors that may occur during the API call
        print(f"Error: {e}")
