#!/usr/bin/env python

import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pydub import AudioSegment

# Converts the mp3 to flac file
file_name = os.path.join(os.path.dirname(__file__),'audio.wav')
#file_name = 'audio.mp3'
sound = AudioSegment.from_mp3(file_name)
file_name = os.path.join(os.path.dirname(__file__),'audio.flac')
#file_name = 'audio.flac'
sound.export(file_name, format='flac', parameters=['-ac', '1'])

# Instantiates a client
client = speech.SpeechClient()

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=22050,
    language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    for result in response.results:
        transcript = format(result.alternatives[0].transcript)
        print (transcript)
