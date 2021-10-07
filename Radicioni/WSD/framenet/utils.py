from nltk.stem import PorterStemmer
import json
from nltk.corpus import framenet as fn
import re

list_input = ['Volubility', 'Coincidence', 'Transfer_scenario', 'Becoming_separated', 'Food']


def stemmer(list_of_words):
    porter = PorterStemmer()
    return [porter.stem(w) for w in list_of_words]


### METODI PER FILE ###

# Creo file da annotare manualmente coi synset attesi
# Nota: per i termini composti 'Transfer_scenario' a mano verranno scelte le parole principali sul file
def create_valutation_file():
    v = {}
    for w in list_input:
        fe_expected_result_dictionary = { fe : "None" for fe in fn.frames(w)[0].FE}
        lu_expected_result_dictionary = { lu : "None" for lu in fn.frames(w)[0].lexUnit}
        v[w] = {'this': None, 'FE': fe_expected_result_dictionary,'LU': lu_expected_result_dictionary}
    with open('valutation_file2.txt', 'w') as f:
        f.write(json.dumps(v, indent=4))


def read_valutation_file():
    with open('valutation_file.txt', 'r') as f:
        data = json.load(f)
    return data


# per parole composte avremo: esempio_esempio[esempio]
# esempio_esempio sarà il termine di framenet
# la parte tra parentesi [] è il termine da usare per cercare su wordnet
def extract_fn_wn_word(term):
    if '[' in term:
        wordnet_word = re.search(r'(?<=\[).+?(?=\])', term).group()
        frame_word = re.search(r'.+?(?=\[)', term).group()
    else:
        frame_word = term
        wordnet_word = term
    return frame_word, wordnet_word