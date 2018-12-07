'''
Serializes word bank
usage: python2 serialize-wordbank [filename]
Author: Christian Roncal
'''

import argparse
import pickle

def serialize(filename, out):
    text = open(filename, 'r').read()
    words = text.split()

    with open(out+'.pkl', 'wb') as handle:
        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename of wordbank")
    parser.add_argument("output", help="output_filename", default="wordbank")
    args = parser.parse_args()
    print "Serialiazing " + args.filename + " to ", args.output + ".pkl"
    serialize(args.filename, args.output)
