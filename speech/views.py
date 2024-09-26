import os
import yt_dlp
import subprocess
from django.conf import settings
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Create your views here.

# WatsonX API setup
WATSON_API_KEY = 'JSW2CVwT_3vFVCJQpj6_PJEB_K-DDwlQHoCvCPzGNV6C'
WATSON_URL = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/b088efec-be09-4d11-8b27-09a420dc010c'

authenticator = IAMAuthenticator(WATSON_API_KEY)
speech_to_text = SpeechToTextV1(authenticator=authenticator)
speech_to_text.set_service_url(WATSON_URL)


def convert_to_wav(input_file):
    """
    Converts any audio/video file to 16kHz WAV format for WatsonX.
    Args:
    input_file: The input file path.
    Returns:
    The path to the converted WAV file.
    """
    output_file = os.path.join(settings.MEDIA_ROOT, 'converted_audio.wav')
    try:
        # Convert the file to 16kHz WAV format suitable for WatsonX
        subprocess.run(
            ['ffmpeg', '-i', input_file, '-ar', '16000', '-ac', '1', output_file],
            check=True
        )
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None


def download_youtube_video_as_wav(url):
    """
    Downloads the YouTube video directly as a WAV file.
    Args:
    url: The YouTube URL.
    Returns:
    The path to the downloaded WAV file.
    """
    output_file = os.path.join(settings.MEDIA_ROOT, 'youtube_audio.wav')
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
            'nopostoverwrites': True
        }],
        'outtmpl': output_file
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_file
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None


def transcribe_audio(file_path):
    """
    Transcribes an audio file using WatsonX Speech to Text service.
    Args:
    file_path: The path to the audio file.
    Returns:
    The transcription result.
    """
    try:
        with open(file_path, 'rb') as audio_file:
            result = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                model='en-US_BroadbandModel'
            ).get_result()
        return result
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


def index(request):
    if request.method == 'POST':
        youtube_url = request.POST.get('url')
        uploaded_file = request.FILES.get('file')

        output_file_path = None
        fs = FileSystemStorage()

        # Handle file upload
        if uploaded_file:
            # Save uploaded file temporarily
            file_path = fs.save(uploaded_file.name, uploaded_file)
            file_full_path = fs.path(file_path)
            print(f"Uploaded file saved at {file_full_path}")

            # Convert uploaded file to WAV format
            output_file_path = convert_to_wav(file_full_path)

        # Handle YouTube URL input
        elif youtube_url:
            # Download YouTube video as WAV
            print(f"Downloading video from YouTube: {youtube_url}")
            output_file_path = download_youtube_video_as_wav(youtube_url)

        # If conversion/download was successful, send the audio to WatsonX for transcription
        if output_file_path and os.path.exists(output_file_path):
            result = transcribe_audio(output_file_path)
            transcribe = [text["alternatives"][0]['transcript'].rstrip() + '.\n' for text in result['results']]

            return render(request, 'home.html', {'transcription': transcribe})

    return render(request, 'home.html')
