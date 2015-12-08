#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hadyelsahar'

"""
running demo script
"""

import argparse
import os
from Vectorizers.wordvectorizer import *

parser = argparse.ArgumentParser(description='a demo script to test the fuctionality of the vectorizer ')
parser.add_argument('-i', '--input', help='input file for the datasets', required=True)
args = parser.parse_args()


s = []
for f in [x for x in os.listdir(args.input) if ".txt" in x]:
    print "processing file : %s" % f
    with file("%s/%s" % (args.input, f), 'r') as fo:
        s.append(fo.read())

vectorizer = WordVectorizer()
X = vectorizer.fit(s)
X = vectorizer.transform(s)















