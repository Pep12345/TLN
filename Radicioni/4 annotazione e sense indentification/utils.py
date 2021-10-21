import os
import csv
import nasari
from pprint import pprint
from babelnet import BabelNetApi
import itertools
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import scipy.stats


def set_nsr_dict():
    global nsr_dict
    nsr_dict = nasari.load_nasari_vectors('utils\mini_NASARI.tsv')


def set_babelnet_api(expected_result):
    global bna
    # Partendo da delle key (word1,word2) le scomponiamo in due liste per poi concatenarle
    # e passarla in input alla classe di babelnet
    l1,l2 = zip(*expected_result.keys())
    bna = BabelNetApi(l1+l2, n=1)


def max_cos_sim(word1, word2, return_type='number'):
    max = -1
    max_sns1 = None
    max_sns2 = None

    sns_word1 = bna.get_synsets_from_word(word1)
    sns_word2 = bna.get_synsets_from_word(word2)
    # per ogni combinazione tra i synsets di word1 e i synsets di word2
    for s1, s2 in itertools.product(sns_word1, sns_word2):

        # estraggo vettori (array numpy) e calcolo similarità
        if not nsr_dict.__contains__(s1) or not nsr_dict.__contains__(s2):
            continue
        array1 = nsr_dict.get(s1).vector()
        array2 = nsr_dict.get(s2).vector()

        # trasformo in matrice perchè sklearn usa matrici per la cosine similarity
        # questa chiamata crea matrice con 1 riga e lunghezza colonne infinito
        array1 = array1.reshape(1, -1)
        array2 = array2.reshape(1, -1)

        # sklearn funziona a matrici ma nel nostro caso avrà un solo elemento
        cs = cosine_similarity(array1, array2)[0][0]

        if cs > max:
            max = cs
            max_sns1 = s1
            max_sns2 = s2

    return max if return_type == 'number' else (max_sns1, max_sns2)


def write_output_file(array,path_file, header):
    np.savetxt(path_file, array, fmt='%s', delimiter="\t", header=header, encoding='utf-8')


def get_terms_from_synset(sns):
    return bna.get_terms_from_synset(sns)