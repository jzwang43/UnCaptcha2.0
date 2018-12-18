'''
Auto-tester
usage: python2 autotester settings
author: christian roncal
'''
import io
import os
import sys

# include upper directory
sys.path.append('..')

import gencaptcha
import argparse
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pydub import AudioSegment
import numpy as np

# author: jizhen wang
def mp3_to_flac(fname):
    file_name = os.path.join(os.path.dirname(__file__), fname)
    #print "filename: ", file_name
    sound = AudioSegment.from_mp3(file_name)
    file_name = os.path.join(os.path.dirname(__file__), fname )
    sound.export(file_name, format='flac', parameters=['-ac', '1'])
    return file_name

def audio_to_text(fname):
    flacfile = mp3_to_flac(fname)

    client = speech.SpeechClient()

    
    transcript = '' 
    with io.open(flacfile, 'rb') as audio_file:
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
             
         
    #print('hs', transcript)
    return transcript
                
def getScore(pred, real):
    score = 0
    for a, i in zip(pred, real):
        score = score + 1 if a == i else score - 1

    if len(pred) > len(real):
        score -= len(pred) - len(real)

    return max(score, 0)

if __name__ == "__main__":
    
    f = open('data.csv', 'w+')
    f.write('captcha_volume,noise_volume,accuracy%\n')
    captcha_vol_range = np.linspace(.5, 2, 8)
    s = 10
    iters = 0

    print 'captcha vol', 'noise vol'
    for cv in captcha_vol_range:

        iters += 1
        for nv in np.linspace(cv - (.40 * cv) , cv, iters):
            print 'processing: ' + str(cv) + ', ' + str(nv)

            settings = {
                'wordbank':'./wordbanks/wordbank.pkl',
                'dir': './captchas/',
                'noise-vol': nv,
                'captcha_vol': cv,
                'nnums': 5
               }
            
            # captcha generator object see gencaptcha.py
            generator = gencaptcha.NumOnWordsCaptchaGenerator(settings)
            # returns a dictionary in form {filename : solution}
            captchas = generator.generate_captchas('captcha', 5)
            predictions = {}
            nsolved = 0

            for fname in captchas.keys():
                pred = audio_to_text(fname) 
                real = captchas[fname].replace(" ", "")
                score =  getScore(pred, real)
                nsolved = nsolved + 1 if getScore(pred, real) > 2 else nsolved

            
            f.write(str(cv) + "," + str(nv) + "," + str(nsolved/5.0) + '\n')

    f.write('\n')
    f.close()
