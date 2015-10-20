__author__ = 'hadyelsahar'

"""
script to preprocess 10K-baseline dataset
"""

import argparse
import re

parser = argparse.ArgumentParser(description='script to preprocess 10K-baseline dataset')
parser.add_argument('-i', '--output', help='input raw file', required=True)
parser.add_argument('-o', '--output', help='output file', required=True)
args = parser.parse_args()


f = open(args.input, 'r')

for l in f.readline():

    # removal of quotes in front and end
    l = re.sub(r"^\"", "", l)
    # removal of in between brackets
    l = re.sub(r"\([^()]*\)", "", l)
    # take first two sentences only
    l = ".".join(l.split(".")[:2]) + " ."
    # replace tabs by
    l = re.sub(r"\t", "\s", l)
    l = re.sub(r"\s+", "\s", l)

print l