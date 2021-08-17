import csv


# Questo metodo serve per i titoli che contengono ; al loro interno
import math


def get_title(row):
    title = ''
    for i in range(1, len(row)):
        # se la cella contiene _ e la seconda parte è numerica è iniziato l'array di pesi
        if '_' in row[i] and row[i].split('_')[1].replace('.','',1).isdigit():
            return i, title
        title += row[i]
    return i, title


# Alcuni elementi di nasari contengono ';' all'interno del lemma quindi li ricostruiamo
def get_array(row):
    result_array = []
    for i, elem in enumerate(row):
        if len(elem) < 1:
            continue
        if '_' in elem:
            result_array.append(elem.split('_'))
        else:
            row[i+1] = elem + ';' + row[i+1]
    return result_array


# Per ogni vettore di nasari aggiungo una riga nella mia dictonary con
#       babelnet id, wikipedia titolo e lista synset
def load_nasari_vectors(file):
    nsr_vct = []
    with open(file, "r", encoding="utf-8") as csv_file:
        for row1 in csv_file:
            row = row1.replace('\n','').split(';')
            i, title = get_title(row)
            try:
                synsets = get_array(row[i:])
            except IndexError:
                print(row[i:])
            try:
                nsr_vct.append(NasariElement(row[0], title, synsets))
            except ValueError as e:
                print(row1)
                exit()
    return nsr_vct


def wo(v1, v2):
    overlap = set(v1.lemmas()).intersection(set(v2.lemmas()))
    if not overlap:
        return 0
    num = sum([float(v1.rank(o) + v2.rank(o))**(-1) for o in overlap])
    den = sum([float(2*i) ** (-1) for i in range(1, len(overlap)+1)])
    return num/den


# La similarità tra due contesti ( liste di vettori di nasari) è data come il massimo delle wo sotto radice
def similarity(v1s, v2s):
    wo_list = [math.sqrt(wo(v1, v2)) for v1 in v1s for v2 in v2s]
    return max(wo_list) if len(wo_list) > 0 else 0


class NasariElement:
    def __init__(self, babelnet_id, wikipedia_title, synsets):
        self.__id = babelnet_id
        self.__title = wikipedia_title
        self.__syn_dict = dict(synsets)
        self.__syn_array = sorted(synsets, key=lambda tup: tup[1])

    def id(self):
        return self.__id

    def syn_array(self):
        return self.__syn_array

    def title(self):
        return self.__title

    def weight(self, lemma):
        return self.__syn_dict.get(lemma)

    def rank(self, lemma):
        tuple = [lemma, self.__syn_dict.get(lemma)]
        return self.syn_array().index(tuple) + 1

    def lemmas(self):
        return list(self.__syn_dict.keys())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'<<NasariElement>id: {self.id()}\t title: {self.title()}\t array: {self.syn_array()}>'