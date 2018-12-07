'''
Takes an pickled/serialized wordbank (array of strings).
can generate words from wordbank as audio files or just speech
Author: Christian Roncal
'''
import random
import pickle
from google.cloud import texttospeech

# pklfname pickle filename, n: number of words
def get_random_wordstr(pklfname, n):
    words = set()
    wordbank = pickle.load(open(pklfname, 'rb'))
    
    while(len(words) < n):
        words.add(random.choice(wordbank))

    return ' '.join(words)

def get_random_numstr(n):
    s = ''

    for num in range(n):
        r = random.randint(0,9)
        s += 'zero ' if r == 0 else str(r) + ' '
    
    return s
