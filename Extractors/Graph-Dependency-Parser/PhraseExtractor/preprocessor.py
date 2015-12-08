__author__ = 'hadyelsahar'

from os import path
import sys

# get to upper directory to append vectorizers
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from Vectorizers.wordvectorizer import *
from nltk.tokenize import TreebankWordTokenizer

_DATA_PATH = __file__.replace("preprocessor.py", "") + "data/"

class Preprocessor:
    """
    preprocessor class is the class responsible of converting the brat annotation
    files into standard outputs of input feature vectors and and
    save them into a pickle file in the 'data' folder
    """
    def __init__(self, inputdir, datadir="./data/", ner=True, pos=True, dependency=False, embeddings="word2vec"):

        self.inputdir = inputdir
        self.datadir = datadir
        self.tokenize = TreebankWordTokenizer().tokenize
        self.vectorizer = WordVectorizer(ner=ner, pos=pos, dependency=dependency, embeddings=embeddings)


        self.S = None
        self.X = None
        self.y = None


    def read_data_dir(self, inputdir):
        """
        :param inputdir: directory contains brat annotation files
        Two files per sentence ending with ".txt" or ".ann"

        .txt : text file contains one sentence per files
        .ann : annotation file contains one Tag or relation per line
        for the scope of phrase extraction we wil concentrate only on lines starting with T
        which are the labeling for TAGS

        :return: (S,X,y)
         S:  array containing all sentences in all the .txt files, in order
         X:  array containing all words tokenized in all .txt files in order i.e. training set labels
         y:  array containing all labels for X in order
        """

        files = os.listdir(inputdir)

        # select only files with annotation existing
        # get the basename without the file type
        # add .txt or .ann later
        file_names = [x.replace(".ann","") for x in if ".ann" in x]

        # capital letters for corpus #small letters per sentence
        S = []
        X = []
        Y = []

        # for every training example
        for f in file_names:

            # collect text sentences tokens
            with file("%s/%s.txt" % (inputdir, f), 'r') as fo:
                s = fo.read()
                x = self.tokenize(s)

            #filling annotations with labels
            with file("%s/%s.ann" % (inputdir, f), 'r') as fa:
                # for every tag in the annotation

                for w in x :
                #################### todo : HERE algorithm match annotations with tokens
                # tokenize every annotated chunk
                # if match in annotation pop  from both queues
                # annotate rest with S or out
                # 
                # if annotation queue is not empty , raise exception


            X.append(x)
            S.append(s)
            Y.append(y)

        return S, X, y




    def vectorize(self, S, X):
        raise NotImplementedError


    def save_data(self, outputdir):
        raise NotImplementedError






