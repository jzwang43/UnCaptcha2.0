'''
creates and tests captchas
author: christian roncal, jizhen wang
'''
import os
import wordstrgen
import speechsynth
import numpy as np
# audiolab will need libsndfile it's a pain to install and IMPOSSIBLE on python3.
from scikits.audiolab import wavread, wavwrite

'''
ensures that both audios have the same length, cuts 
longer one otherwise.
author: christian roncal
'''
def ensure_equal_length(noise, captcha):
    return noise[:len(captcha)]

def ensure_dir(dirname):
    if(not os.path.exists(dirname)): os.mkdir(dirname)

'''
generates a number captcha with word noise
author: jizhen wang, christian roncal
TODO: clean up parameters by using iterables
TODO: make default variables/constants
'''
class NumOnWordsCaptchaGenerator:
    def __init__(self, settings):
        self.wordbank = settings['wordbank']
        self.outputdir = settings['dir']
        self.noise_vol = settings['noise-vol']
        self.captcha_vol = settings['captcha_vol']
        self.nnums = settings['nnums']
        self.nwords = self.nnums + 1

        ensure_dir(self.outputdir)

    '''
    generates a number captcha with word noise
    author: jizhen wang, christian roncal
    TODO: clean up parameters by using iterables
    TODO: make default variables/constants
    '''
    def new_numeral_captcha_on_words(self, fname):
        wordstr = wordstrgen.get_random_wordstr(self.wordbank, self.nwords)
        numstr = wordstrgen.get_random_numstr(self.nnums)
        
        ensure_dir('temp')
        #these are the filenames of the audio files
        wordaudio = speechsynth.make_audio(wordstr, 'words', './temp/')
        numaudio = speechsynth.make_audio(numstr, 'nums', './temp/')

        # read audio data 
        wordaudio_data, fs_word, enc_word = wavread(wordaudio)
        numaudio_data, fs_num, enc_num = wavread(numaudio)

        wordaudio_data = ensure_equal_length(wordaudio_data, numaudio_data)

        # combine audio data modifying volumes
        captcha_audio =  self.noise_vol * wordaudio_data + self.captcha_vol * numaudio_data
        
        outputfname = self.outputdir + fname

        if(os.path.exists(outputfname)): os.remove(outputfname)

        wavwrite(captcha_audio, outputfname, 22050)
        
        # return output filename and the answer
        return outputfname, numstr
    

    '''
    genreate multiple captchas
    '''
    def generate_captchas(self, fname, n = 1):
        res = {}
        for i in range(n):
            captcha = self.new_numeral_captcha_on_words(fname + str(i)+".wav")
            res[captcha[0]] = captcha[1]

        return res


#    if __name__ == "__main__":
#       settings = {
#                   'wordbank':'./wordbanks/wordbank.pkl',
#                   'dir': './captchas/',
#                   'noise-vol': .54,
#                   'captcha_vol': 1.2,
#                   'nnums': 5
#                  }
#       generator = NumOnWordsCaptchaGenerator(settings)
#       generator.generate_captchas('test', 3)
#   
#
