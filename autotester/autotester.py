'''
Auto-tester
usage: python2 autotester settings
author: christian roncal
'''
import io
import os
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', help='captcha method', default='numonwords', required=False)
    parser.add_argument('--wordbank', help="full path of wordbank", default='./wordbanks/wordbank.pkl', required=False)
    parser.add_argument('--outputdir', help="full path of output dir", default='./captchas/', required=False)
    parser.add_argument('--noisepercent', help="percent of noise", default='.55', required=False)
    parser.add_argument('--captchapercent', help="percent of captcha", default='1.1', required=False)
    parser.add_argument('--filename:', help="filenameX.wav", default='captcha', required=False)
    parser.add_argument('--ncaptcha', help='number of captchas', default=10, required=False)
    args = parser.parse_args() 
    

    settings = {
           'wordbank':'./wordbanks/wordbank.pkl',
           'dir': './captchas/',
           'noise-vol': .6,
           'captcha_vol': 1.125,
           'nnums': 5
          }

#    settings = {
#           'wordbank':args.wordbank,
#           'dir': args.outputdir,
#           'noise-vol': args.noisepercent,
#           'captcha_vol': args.captchapercent,
#           'nnums': args.ncaptcha
#          }
#
#    generator = gencaptcha.NumOnWordsCaptchaGenerator(settings)
#    captchas = generator.generate_captchas(args.filename, args.ncaptcha)
#    predictions = {}
#
    generator = gencaptcha.NumOnWordsCaptchaGenerator(settings)
#   captchas = generator.generate_captchas('captcha', 5)
    predictions = {}
    nsolved = 0
    
    for fname in captchas.keys():
        pred = audio_to_text(fname) 
        real = captchas[fname].replace(" ", "")
        score =  getScore(pred, real)
        print "prediction: ", pred
        print "actual: ", real
        print "score: ", score
        nsolved = nsolved + 1 if getScore(pred, real) > 2 else nsolved

    
    print "solved: " + str(nsolved) + " ; gstt success rate: " + str(nsolved / 5.0)


