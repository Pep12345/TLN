import math
import csv
import numpy as np


def __get_synset_and_name(name):
    n = name.split('__')
    return n[0], n[1].replace('_',' ')


def load_nasari_vectors(file):
    nsr_dict = {}
    with open(file, "r", encoding="utf-8") as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')

        for row in tsv_reader:
            synset, name = __get_synset_and_name(row[0])
            # creo array numpy per agevolare libreria sklearn in cosine_similarity
            # inoltre uso funzione map per converire stringa -> float
            vector = np.array(list(map(float, row[1:])))
            try:
                nsr_dict[synset] = NasariElement(synset, name, vector)
            except ValueError as e:
                print(row)
                exit()

    return nsr_dict


class NasariElement:

    def __init__(self, synset, name, vector):
        self.__bn_syn = synset
        self.__name = name
        self.__vector = vector

    def id(self):
        return self.__bn_syn

    def vector(self):
        return self.__vector

    def name(self):
        return self.__name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'<<NasariElement> Synset: {self.id()}\t title: {self.name()}\t array: {self.vector()}>'