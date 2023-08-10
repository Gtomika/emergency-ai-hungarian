import audio
import speech
import chatgpt

DEBUG = False
RECORDING_FILE_NAME = 'felvetel.wav'

if __name__ == '__main__':
    if DEBUG:
        audio.list_audio_devices()
    audio.record_audio(filename=RECORDING_FILE_NAME)
    print(f'A felvétel elkészült és mentve lett a "{RECORDING_FILE_NAME}" fájlba')

    transcript = speech.transcribe_speech(filename=RECORDING_FILE_NAME)
    print('\nAz átirat:\n------------------------------------------------------------')
    print(transcript)
    print('------------------------------------------------------------')

    emergency_response = chatgpt.generate_emergency_call_response(transcript)

    print('\nA hívás részletei:\n------------------------------------------------------------')
    print(f'- Típus: {emergency_response.emergency_type}')
    print(f'- Hely: {emergency_response.location if emergency_response.location is not None else "Nem azonosítható"}')
    print(f'- Javasolt válasz: {emergency_response.message}')
    print('------------------------------------------------------------')

    audio_bytes = speech.synthesize_speech(emergency_response.to_detailed_string_hungarian())
    audio.play_audio(audio_bytes)

    print('AI asszisztens válasza lejátszva.')
    print('A vészhelyzeti hívás szimuláció befejeződött.')


