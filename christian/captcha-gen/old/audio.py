

"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
from google.cloud import texttospeech
import re
import subprocess

file = open('wordbank.txt', 'r')
text = file.read()
re.sub(r'[^\w\s]','',text)
words=text.split()
#words = [word.strip(string.punctuation) for word in text.split()]
#print(words)
from random import randint
index = randint(0, len(words) - 4)
string = words[index]
while len(string) < 20:
	index += 1
	string += ' ' + words[index - 1] 
print(string)

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.types.SynthesisInput(text=string)

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.types.VoiceSelectionParams(
    language_code='en-US',
    ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

# Select the type of audio file you want returned
audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
response = client.synthesize_speech(synthesis_input, voice, audio_config)

# The response's audio_content is binary.
import os
if os.path.exists('output.wav'):
	os.remove('output.wav')
with open('output.wav', 'w+') as out:
    # Write the response to the output file.
    out.write(str(response.audio_content))
    #print('Audio content written to file "output.wav"')
    

# noise = ''.join(["%s " % randint(0, 9) for num in range(0, 6)])

def get_num_str(n):
   s = ''
   for num in range(n):
       r = randint(0, 9)
       s += 'zero ' if r == 0 else str(r) + ' '
   return s

noise = get_num_str(6)
print("noise: ", noise)
synthesis_input = texttospeech.types.SynthesisInput(text=noise)

response = client.synthesize_speech(synthesis_input, voice, audio_config)
if os.path.exists('noise.wav'):
	os.remove('noise.wav')

# The response's audio_content is binary.
with open('noise.wav', 'w+') as out:
    # Write the response to the output file.
    out.write(str(response.audio_content))
    #print('Audio content written to file "noise.wav"')

import numpy as np
from scikits.audiolab import wavread, wavwrite #might need libsndfile

data1, fs1, enc1 = wavread('output.wav')
data2, fs2, enc2 = wavread('noise.wav')
assert fs1 == fs2
assert enc1 == enc2
if (len(data1) < len(data2)):
    data2 = data2[:len(data1)]


result = 0.65 * data1 + 1 * data2
wavwrite(result, 'audio.wav', 22050)

python3_command = "python rec.py"  # launch your python2 script using bash
process = subprocess.Popen(python3_command.split(), stdout=subprocess.PIPE)
process.wait()
output = process.stdout.readline().decode('utf-8');
print(output)
