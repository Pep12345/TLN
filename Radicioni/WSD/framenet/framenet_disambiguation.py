from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import os
import nltk
import similarity_and_wsd.wsd_ex as wsd
'''
    student: Biondi
        ID:   44	frame: Volubility
        ID: 1812	frame: Coincidence
        ID: 1192	frame: Transfer_scenario
        ID: 1863	frame: Becoming_separated
        ID:  277	frame: Food
'''
list_input = ['Volubility', 'Coincidence', 'Transfer_scenario', 'Becoming_separated', 'Food']
wn_input = ['Volubility', 'Coincidence', 'Transfer', 'Becoming', 'Food']

def check_similarity(word, frame):
    return wsd.simplified_lesk(word, frame.definition)


if __name__ == "__main__":
    wsd.read_stop_words()
    for i in range(0,5):
        best_sense = check_similarity(wn_input[i], fn.frames(list_input[i])[0])
        print(best_sense)
    exit()
    for input in list_input:
        print(len(fn.frames(input)))
        frame = fn.frames(input)[0]
        print(frame.name)
        print(frame.definition)
        print(frame.FE)
        print(frame.lexUnit.keys())
