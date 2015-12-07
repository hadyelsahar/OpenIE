#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hadyelsahar'

"""
running demo script
"""

import argparse
import cPickle
import xml.etree.ElementTree as ET
import os


parser = argparse.ArgumentParser(description='a demo script to test the fuctionality of the vectorizer ')
parser.add_argument('-i', '--input', help='input file for the datasets', required=True)
args = parser.parse_args()


for l in file(args.input, 'r').readlines():

    try:
        root = ET.fromstring(l)
    except Exception as e:
        # print "error parsing xml line :\n %s" % l
        continue
    labels = [c.tag for c in root]
    words = [c.text for c in root]

    x1.append(words)
    x3.append(labels)
    for w in words:
        u_words.add(w)
    for l in labels:
        u_labels.add(l)


# dict1 = {"O": 0, "B-Subj": 1, "I-Subj": 2, "B-Pred": 3, "I-Pred": 4, "B-Obj": 5, "I-Obj": 6}
dict1 = {v: k for k, v in enumerate(u_labels)}  # more generic to any tag labels
dict2 = {}
dict3 = {v: k for k, v in enumerate(u_words)}


for i, s in enumerate(x3):
    for j, _ in enumerate(s):
        x1[i][j] = dict3[x1[i][j]]   # replacing each word by it's index from word2idx dict3
        x3[i][j] = dict1[x3[i][j]]   # replacing each tag by it's tag index from label2idx dict1

data = [x1, x2, x3]
dicts = {'labels2idx': dict1, 'tables2idx': dict2, 'words2idx': dict3}

print "finished preparing data with: \n %s sentences \n %s unique words " %(len(x1), len(dict3))
print "loading data into pkl file : %s ..." % args.output

cPickle.dump((data, dicts), open(args.output, 'w'))

print "done."















