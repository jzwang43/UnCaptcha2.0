#!/usr/bin/env python3

from gtts import gTTS
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--out_file", nargs="?", help="file to store text into", default="audio.mp3")
parser.add_argument("-s", "--string", nargs="?", help="String to be recorded as audio")
parser.add_argument("-l", "--language", nargs="?", help="Language for the noise to be saved as.", default="en")
args = parser.parse_args()

s = args.string
f = args.out_file
l = args.language

tts = gTTS(text=s, lang=l)
tts.save(f)
os.system("afplay %s" % f)

