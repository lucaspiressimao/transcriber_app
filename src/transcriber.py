import speech_recognition as sr
import openai
from pydub import AudioSegment
import tempfile
import os

def transcribe_audio(file_path, api_key, send_to_openai=True):
    recognizer = sr.Recognizer()

    # Check if the M4A file needs to be converted to WAV
    if file_path.endswith('.m4a'):
        # Create a temporary file for the audio in WAV format
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            audio = AudioSegment.from_file(file_path, format="m4a")
            audio.export(temp_wav.name, format="wav")
            audio_file_path = temp_wav.name
    else:
        audio_file_path = file_path

    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        audio_text = recognizer.recognize_google(audio, language="en-US")

        if send_to_openai:
            openai.api_key = api_key

            # Open the temporary or original WAV file to send to OpenAI
            with open(audio_file_path, "rb") as audio_file:
                response = openai.Audio.transcribe("whisper-1", audio_file)
                return response['text']
        else:
            return audio_text

    except sr.UnknownValueError:
        return "Could not understand the audio"
    except sr.RequestError as e:
        return f"Request error; {e}"
    finally:
        # Remove the temporary file if it was created
        if file_path.endswith('.m4a') and os.path.exists(audio_file_path):
            os.remove(audio_file_path)
