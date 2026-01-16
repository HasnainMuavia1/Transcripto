**🚀 Transcripto 🚀**

**Transcripto** is a Django-based application designed to transcribe videos to text, supporting multiple languages using a custom model. The platform allows users to either upload their own videos or provide a YouTube URL for transcription. 🎥📝

**Features**

- **Multiple Language Support**: Transcribe videos in different languages using Watson API.
- **Video Upload**: Upload your own video files for transcription.
- **YouTube URL**: Enter a YouTube video URL and get the transcription in just a few clicks.
- **AI-Powered**: Built to showcase AI capabilities, even though web development isn’t my strong suit!

**Tech Stack**

- **Backend**: Django (Python 3.10)
- **Frontend**: Custom UI design (inspired by a UI/UX design concept)
- **Transcription Engine**: IBM Watson Speech to Text API
- **Video Processing**: ffmpeg

**Installation**

**Requirements**

Make sure you have the following dependencies installed:

1. [ffmpeg](https://ffmpeg.org/download.html)
1. [ibm_watson](https://pypi.org/project/ibm-watson/)
1. [python 3.10](https://www.python.org/downloads/release/python-310/)
1. [ibm_cloud_sdk_core](https://pypi.org/project/ibm-cloud-sdk-core/)

**Steps to Run Locally**

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the root directory and add your configuration:

   ```env
   SECRET_KEY='your_django_secret_key'
   DEBUG=True
   WATSON_API_KEY='your_ibm_watson_api_key'
   WATSON_URL='your_ibm_watson_url'
   ```

3. **Run the server**

   ```bash
   python manage.py runserver
   ```
