# -*- coding: utf-8 -*-
__author__ = 'hadyelsahar'


import numpy as np
import gensim

from sklearn.base import TransformerMixin
from nltk.util import ngrams
from nltk.tokenize import TreebankWordTokenizer
from scipy.sparse import *


_W2V_BINARY_PATH = __file__.replace("wordvectorizer.py", "") + "word2vec/GoogleNews-vectors-negative300.bin.gz"

class WordVectorizer(TransformerMixin):

    def __init__(self, ner=True, pos=True, dependency=False, embeddings="word2vec", tokenizer = None):
        """

        :param ner: Boolean indicating adding named entity recognition features in the feature vector or not
        :param pos: Boolean indicating adding part of speech tagging in the features in the feature vector or not
        :param dependency: Boolean to add dependency features or not
        :param embeddings: name of which word vectors to use, default word2vec
        :return:
        """
        if tokenizer is None:
            self.tokenize = TreebankWordTokenizer.tokenize

        if embeddings == "word2vec":
            self.model = gensim.models.Word2Vec.load_word2vec_format(_W2V_BINARY_PATH, binary=True)

        self.ner = ner
        self.pos = pos
        self.dependency = dependency


    def transform(self, sentences, **transform_params):
        """
        :param X: iterator of sentences
        :param transform_params:
        :return: csr matrix each row contains a word (tokenized using standard tokenizer)
         in sequence and columns indicating feature vector.
        """
        feature_vector_size = 0
        if self.pos:
            feature_vector_size += 1
        if self.ner:
            feature_vector_size += 1
        if self.model:
            feature_vector_size += self.model.vector_size

        # large matrix containing words per row and features per column
        X = np.zeros((0, feature_vector_size), np.float32)
        word_list = []
        for s in sentences:
            tokens = self.tokenize(s)
            word_list += tokens

            if self.model:
                wordvec = np.zeros((len(tokens), self.model.vector_size), np.float32)
                for i, w in enumerate(tokens):
                    wordvec[i] = self.word2vec(w)

            if self.pos:
                posvec = np.zeros((len(tokens), 1), np.float32)
                pass

            if self.ner:
                nervec = np.zeros((len(tokens), 1), np.float32)
                pass

            if self.dependency:
                pass

            # matrix nxm
            # n : number of words in in a sentence
            # m : number of features per word
            words_features = np.hstack([wordvec, posvec, nervec])
            X = np.vstack([X, words_features])

        return csr_matrix(X), word_list

    def fit(self, X, y=None, **fit_params):
        return self

    def word2vec(self, word):
        """
        using loaded word2vec model given a vector return it's equivalent word2vec representation
        if word is not existing, replace by zero vector
        todo: retrain existing word2vec with the training data sentences to handle unseen words
        :param word: word
        :return: raw numpy vector of a word dtype = float32
        """
        if word in self.model:
            return self.model[word]
        else:
            return np.zeros(self.model.vector_size, np.float32)

