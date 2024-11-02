import speech_recognition as sr
import openai
from pydub import AudioSegment
import tempfile
import os

def transcribe_audio(file_path, api_key, send_to_openai=True):
    recognizer = sr.Recognizer()

    # Verifica se precisa converter o arquivo M4A para WAV
    if file_path.endswith('.m4a'):
        # Cria um arquivo temporário para o áudio em formato WAV
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            audio = AudioSegment.from_file(file_path, format="m4a")
            audio.export(temp_wav.name, format="wav")
            audio_file_path = temp_wav.name
    else:
        audio_file_path = file_path

    with sr.AudioFile(audio_file_path) as source:
        audio = recognizer.record(source)

    try:
        audio_text = recognizer.recognize_google(audio, language="pt-BR")

        if send_to_openai:
            openai.api_key = api_key

            # Abre o arquivo WAV temporário ou original para enviar para o OpenAI
            with open(audio_file_path, "rb") as audio_file:
                response = openai.Audio.transcribe("whisper-1", audio_file)
                return response['text']
        else:
            return audio_text

    except sr.UnknownValueError:
        return "Não foi possível entender o áudio"
    except sr.RequestError as e:
        return f"Erro na solicitação; {e}"
    finally:
        # Remove o arquivo temporário se foi criado
        if file_path.endswith('.m4a') and os.path.exists(audio_file_path):
            os.remove(audio_file_path)

