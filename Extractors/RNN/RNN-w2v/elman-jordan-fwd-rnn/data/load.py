import gzip
import cPickle
import urllib
import os
import random
import numpy as np

from os.path import isfile

PREFIX = os.getenv('ATISDATA', '')

def download(origin):
    '''
    download the corresponding atis file
    from http://www-etud.iro.umontreal.ca/~mesnilgr/atis/
    '''
    print 'Downloading data from %s' % origin
    name = origin.split('/')[-1]
    urllib.urlretrieve(origin, name)

def load(filename):
    # if not isfile(filename):
    #     download('http://www-etud.iro.umontreal.ca/~mesnilgr/atis/'+filename)
    f = open(filename, 'rb')
    return f

def atisfull(fname):
    f = load(fname)
    train_set, test_set, dicts = cPickle.load(f)
    return train_set, test_set, dicts

def atisfold(fname):
    # assert fold in range(5)
    f = load(fname)
    data, dicts = cPickle.load(f)
    words, _, labels = data
    words = np.array(words)
    labels = np.array(labels)

    train_ids,  valid_ids, test_ids = get_train_valid_test_folds(range(0, len(words)), test_size=0.1, valid_size=0.1)
    train_set = [words[train_ids], _, labels[train_ids]]
    valid_set = [words[valid_ids], _, labels[valid_ids]]
    test_set = [words[test_ids], _, labels[test_ids]]

    return train_set, valid_set, test_set, dicts

def get_train_valid_test_folds(ids, test_size, valid_size, rand_state=2):
    """
    method takes the data ids and return train, valid, test splits according to which fold
    :param data ids
    :param test_size: size from 0 -> 1 of the test set
    :param valid_size: size from 0 -> 1 of the validation set or None for no validation
    :param fold: fold number
    :return: three arrays containing ids of training, testing, validation splits (train_ids, test_ids, valid_ids)
    or (train_ids, test_ids) if valid = None
    """
    if valid_size:
        if test_size + valid_size >= 1:
            raise ValueError('The sum of the testing and validation sets should be less than 1')
    elif test_size >= 1:
        raise ValueError('The value of the testing set should be less than 1')

    random.seed(rand_state)
    random.shuffle(ids)

    test_size = int(round(test_size * len(ids)))  # convert percentage to numbers
    test_ids = ids[0:test_size]

    if valid_size:
        valid_size = int(round(valid_size * len(ids)))
        valid_ids = ids[test_size:test_size + valid_size]
        train_ids = ids[test_size + valid_size:]
        return train_ids, valid_ids, test_ids
    else:
        train_ids = ids[test_size:]
        return train_ids, test_ids


if __name__ == '__main__':
    
    ''' visualize a few sentences '''

    import pdb
    data = atisfull()

    w2ne, w2la = {}, {}
    train, test, dic = data
    
    w2idx, ne2idx, labels2idx = dic['words2idx'], dic['tables2idx'], dic['labels2idx']
    
    idx2w  = dict((v,k) for k,v in w2idx.iteritems())
    idx2ne = dict((v,k) for k,v in ne2idx.iteritems())
    idx2la = dict((v,k) for k,v in labels2idx.iteritems())

    test_x,  test_ne,  test_label  = test
    train_x, train_ne, train_label = train
    wlength = 35

    for e in ['train','test']:
      for sw, se, sl in zip(eval(e+'_x'), eval(e+'_ne'), eval(e+'_label')):
        print 'WORD'.rjust(wlength), 'LABEL'.rjust(wlength)
        for wx, la in zip(sw, sl): print idx2w[wx].rjust(wlength), idx2la[la].rjust(wlength)
        print '\n'+'**'*30+'\n'
        pdb.set_trace()
