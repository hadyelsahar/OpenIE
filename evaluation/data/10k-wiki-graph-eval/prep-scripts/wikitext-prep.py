__author__ = 'hadyelsahar'

"""
script to preprocess wikitext and create a 10K- dataset
one sentence per line 
removal of short sentences (remove all that less than 10 words)

"""

import argparse
import re
import codecs

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.tag import StanfordPOSTagger

###############
# GLOBAL VARS #
###############
st = StanfordPOSTagger('english-bidirectional-distsim.tagger') 


#########################
# Preprocessing Methods #
#########################

def picksentences(l, minwords=15):
    """
    take a wikipedia text document do all necessary preprocessing 
    and return a list of candidate sentences 
    that have more than `minwords` word`
    """
    
    # removal of in between brackets and fwd slashes
    l = re.sub(r"\([^)]+\)", "", l)
    l = re.sub(r"/[^/]+/", " ", l)
    # replace tabs by space
    l = re.sub(r"\t", " ", l)
    # removal of extra spaces
    l = re.sub(r"\s+", " ", l)
    # removal of extra lines
    l = re.sub(r"\n+", "\n", l)
    l = re.sub(r"\n", ". ", l)
    l.strip()
    
    return [s for s in sent_tokenize(l) if len(word_tokenize(s)) > minwords ]
    

def getpostags(l):
    """
    gets a sentence and returns a list of pos tags
    """
    pos = st.tag(word_tokenize(l))
    # pos = nltk.pos_tag(word_tokenize(l))
    return [p[1] for p in pos]
    
#########################
## ARGUMENT DEFINITION ##
#########################
parser = argparse.ArgumentParser(description='script to preprocess 10K-baseline dataset')
parser.add_argument('-i', '--input', help='input raw file', required=True)
parser.add_argument('-o', '--output', help='output file', required=True)
args = parser.parse_args()



fin = codecs.open(args.input, encoding="utf-8")
fout = codecs.open(args.output, 'w', encoding="utf-8")


txt = unicode(fin.read())

SENT_CNT = 0 

for i in re.finditer(r"<doc.*url=(\".*\").*title=(\".*\")>([^<]+)</doc>", txt):
    url  = i.group(1)
    title = i.group(2)
    l = i.group(3)

    # extraction of candidate sentences from wikipedia articles 
    s = picksentences(l)
    fout.write("\n".join(s))

    # pos = []
    
    # for i in s:
    #     SENT_CNT += 1 
    #     print SENT_CNT
    #     pos.append(getpostags(i))

    # fout.write("\n".join([" ".join(l) for l in pos]))

fin.close()
fout.close()