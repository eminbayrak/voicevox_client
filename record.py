import os
import pyaudio
import wave
from datetime import datetime
import keyboard
import subprocess
import deepl
import requests
import urllib.parse
import winsound

# Set the base URL for the Voicevox API
base_url = 'http://192.168.1.247:50021'

# Create a DeepL translator object
translator = deepl.Translator('53dbe3f7-3e14-5dbb-0689-c26e3e977575:fx')


def record(output_filename):
    # CHUNK = 1024
    # FORMAT = pyaudio.paInt16
    # CHANNELS = 1
    # RATE = 44100
    CHUNK = 512
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 22050

    audio = pyaudio.PyAudio()

    is_recording = False
    frames = []

    while True:
        if keyboard.is_pressed('r') and not is_recording:
            print('Recording started')
            is_recording = True
            frames = []
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                                rate=RATE, input=True,
                                frames_per_buffer=CHUNK)
            continue

        if not keyboard.is_pressed('r') and is_recording:
            print('Recording stopped')
            is_recording = False
            stream.stop_stream()
            stream.close()
            audio.terminate()

            # Save audio as WAV file
            filename = f'{output_filename}.wav'
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            # Call the Whisper AI to transcribe the audio
            subprocess.run(["whisper", filename, "--language", "en"])

            # Remove the temporary WAV file
            os.remove(filename)

            with open("output.txt", "r") as f:
                text = f.read()
            english_text = text

            # Translate the English text to Japanese
            japanese_text = translator.translate_text(
                english_text, target_lang='JA')
            print(f'(Japanese text: {japanese_text}')

            # Call VoiceVox Engine
            speaker_id = '5'  # Character voice id
            params_encoded = urllib.parse.urlencode(
                {'text': japanese_text, 'speaker': speaker_id})
            req = requests.post(f'{base_url}/audio_query?{params_encoded}')
            req.raise_for_status()  # raise an error if the status code is not in the 200-299 range
            query = req.json()
            query['volumeScale'] = 4.0
            query['intonationScale'] = 1.5
            query['prePhonemeLength'] = 1.0
            query['postPhonemeLength'] = 1.0
            # synthesize voice as wav file
            params_encoded = urllib.parse.urlencode({'speaker': speaker_id})
            req = requests.post(
                f'{base_url}/synthesis?{params_encoded}', json=query)
            req.raise_for_status()  # raise an error if the status code is not in the 200-299 range
            speech_filename = 'speech.wav'
            with open(speech_filename, 'wb') as outfile:
                outfile.write(req.content)
            # play audio file
            winsound.PlaySound(speech_filename, winsound.SND_FILENAME)

        if is_recording:
            data = stream.read(CHUNK)
            frames.append(data)


if __name__ == '__main__':
    record('output')
