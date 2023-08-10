import threading
import queue

import pyaudio
import wave

audio = pyaudio.PyAudio()

# probably different on other computers
SPEAKER_DEVICE_INDEX = 4
MICROPHONE_DEVICE_INDEX = 14

# depends on what your input/output devices support
INPUT_SAMPLE_RATE = 16000
INPUT_CHANNELS = 2

OUTPUT_SAMPLE_RATE = 16000
OUTPUT_CHANNELS = 1

CHUNK_SIZE = 1024

frames = []

def record_audio(filename: str):
    global frames
    audio_format = pyaudio.paInt16

    stream = audio.open(format=audio_format,
                        channels=INPUT_CHANNELS,
                        rate=INPUT_SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    frames = []

    print("Az Enterrel kezdheted meg a felvételt...")
    input()  # Wait for the user to press Enter to start recording

    input_queue = queue.Queue()
    recording_thread = threading.Thread(target=__start_recording, args=(stream, CHUNK_SIZE, input_queue))
    recording_thread.start()

    print("Felvétel elindult... nyomd meg az Entert a leállításhoz")
    input()
    input_queue.put(None)  # Signal the recording thread to stop

    recording_thread.join()  # Wait for the recording thread to finish
    print("Felvétel befejeződött")

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()

    frame_bytes = b''.join(frames)
    wf = wave.open(filename, 'wb')
    wf.setnchannels(INPUT_CHANNELS)
    wf.setsampwidth(audio.get_sample_size(audio_format))
    wf.setframerate(INPUT_SAMPLE_RATE)
    wf.writeframes(frame_bytes)
    wf.close()

def __start_recording(stream, chunk_size, input_queue):
    global frames
    frames = []
    while True:
        data = stream.read(chunk_size)
        frames.append(data)
        if not input_queue.empty():
            break

def list_audio_devices():
    print("Available audio devices:")
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        device_name = device_info['name']
        print(f"Device {i}: {device_name}")
        print("Supported configurations:")
        print(f"Channels: {device_info['maxInputChannels']}")
        print(f"Sample Rate: {device_info['defaultSampleRate']} Hz")
        print("-----")

def play_audio(audio_bytes):
    print('Hang lejátszása...')
    stream = audio.open(format=pyaudio.paInt16,
                        channels=OUTPUT_CHANNELS,
                        rate=OUTPUT_SAMPLE_RATE,
                        output=True)

    index = 0
    while index < len(audio_bytes):
        chunk = audio_bytes[index:index + CHUNK_SIZE]
        stream.write(chunk)
        index += CHUNK_SIZE

    stream.stop_stream()
    stream.close()

# print(audio.get_default_output_device_info())
# print(audio.get_default_input_device_info())
# list_audio_devices()
# #record_audio('felvetel.wav')
# with open('felvetel.wav', 'rb') as audio_file:
#     audio_bytes = audio_file.read()
#     play_audio(audio_bytes)
# audio.terminate()