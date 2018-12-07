import wordsgen
import speechsynth

wordstr = wordsgen.get_random_wordstr('wordbank.pkl', 3)
print(speechsynth.make_audio(wordstr, 'testing'))
