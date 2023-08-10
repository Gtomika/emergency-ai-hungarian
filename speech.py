import openai
from google.cloud.texttospeech_v1 import TextToSpeechClient, SynthesisInput, VoiceSelectionParams, AudioConfig, \
    SynthesizeSpeechRequest

import audio

tts_client = TextToSpeechClient()

def transcribe_speech(filename: str):
    print(f'Átirat elkészítése a {filename} fájlból az OpenAI transcribe szolgáltatással...')
    with open(filename, 'rb') as audio_file:
        response = openai.Audio.transcribe("whisper-1", audio_file)
        return response['text']

def synthesize_speech(text: str):
    print('Szöveg küldése a Google Cloud TTS szolgáltatásnak...')

    input = SynthesisInput()
    input.text = text

    voice = VoiceSelectionParams()
    voice.language_code = "hu-HU"

    audio_config = AudioConfig()
    audio_config.audio_encoding = "LINEAR16"
    audio_config.sample_rate_hertz = audio.OUTPUT_SAMPLE_RATE

    request = SynthesizeSpeechRequest(
        input=input,
        voice=voice,
        audio_config=audio_config,
    )

    # Make the request
    response = tts_client.synthesize_speech(request=request)
    audio_bytes = response.audio_content
    print(f'Beszéd sikeresen szintetizálva {len(audio_bytes)} bájt méretben')
    return audio_bytes

# audio.list_audio_devices()
# audio_bytes = synthesize_speech('Szia! Én a Google felhőből szólok hozzád.')
# audio.play_audio(audio_bytes)