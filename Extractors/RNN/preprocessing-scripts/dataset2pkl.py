#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'hadyelsahar'

"""
This script is to take any dataset for IOB annotation and
convert it to pickle file to be loaded directly to the NN

##############
# input file #
##############
is one sentence per line in the form of
<O>that</O> <B-Subj>they</B-Subj> <B-Pred>gain</B-Pred> <B-Obj>most</B-Obj> \
<I-Obj>of</I-Obj> <I-Obj>external</I-Obj> <I-Obj>sources</I-Obj> .

###############
# output file #
###############
#pickle file is created as follows

data  = [x1,x2,x3]
x1 = 2d matrix containing word-ids of every word in every sentence
x2 = []
x3 = 2d matrix containing label index of every word in every sentence

dict1 = {"labelname":index}
dict2 = {#named entities.. can exclude and put as empty}
dict3 = {"word":index}
dicts = {'labels2idx':dict1, 'tables2idx':dict2, 'words2idx':dict3}

picklefile = (data, dicts)

"""

import argparse
import cPickle
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser(description='a script to convert datasets into a pickle file to load to the RNN')
parser.add_argument('-i', '--input', help='input file for the datasets', required=True)
parser.add_argument('-o', '--output', help='output file directory', required=True)
args = parser.parse_args()

# loading data and putting it in the structure described in the file comments
u_words = set()   # unique words, better do it like that to avoiding extra time to unique the whole dataset
u_labels = set()  # all unique labels in the dataset

x1 = []
x2 = []
x3 = []

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















