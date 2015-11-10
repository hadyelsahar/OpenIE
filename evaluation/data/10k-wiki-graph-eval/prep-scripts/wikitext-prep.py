__author__ = 'hadyelsahar'

"""
script to preprocess wikitext and create a 10K- dataset
one sentence per line 
removal of short sentences (remove all that less than 10 words)

"""

import argparse
import re
import nltk


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

    return [s for s in l.split(". ") if len(s.split(" ")) > minwords ]
    
def getpostags(l)
    """
    gets a sentence and returns a list of pos tags
    """
    
    return pos
    

#########################
## ARGUMENT DEFINITION ##
#########################
parser = argparse.ArgumentParser(description='script to preprocess 10K-baseline dataset')
parser.add_argument('-i', '--input', help='input raw file', required=True)
parser.add_argument('-o', '--output', help='output file', required=True)
args = parser.parse_args()



fin = open(args.input)
fout = open(args.output,'w')


txt = fin.read()
for i in re.finditer(r"<doc.*url=(\".*\").*title=(\".*\")>([^<]+)</doc>", txt):
    url  = i.group(1)
    title = i.group(2)
    l = i.group(3)

    s = picksentences(l)
    fout.write("\n".join(s))

fin.close()
fout.close()