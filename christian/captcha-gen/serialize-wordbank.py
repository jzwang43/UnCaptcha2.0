'''
Serializes word bank
usage: python2 serialize-wordbank [filename]
Author: Christian Roncal
'''

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename of wordbank")
    parser.add_arguemtn("output", help="output_filename", default="wordbank")
    args = parser.parse_args()
    print("Serialiazing ", args.filename, "to ", args.output + ".pkl")
    serialize(args.filename)
