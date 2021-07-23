from nltk.corpus import wordnet as wn
import csv, os, math
import numpy as np
import scipy.stats
## domande
 ## 1) money,cash è ripetuta nel dataset
 ## 2) posso usare formule similarità wn o devo scriverle a mano?
 ## perchè dog[1] come antenato comunet usando wordnet da frump che però fa parte dello stesso synset e non è un antenato?
 ## path similarity non ha senso
 ## lch non funziona tra pos diversi


def read_csv(file_name):
    dict = {}
    keys = []
    target_result = []
    dir = os.path.dirname(os.path.abspath(__file__))
    with open(dir + '/' + file_name, "r") as csv_file:
        csv_file.readline()
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            #if(dict.__contains__((row[0],row[1]))): print((row[0],row[1]))
            dict[(row[0],row[1])] = float(row[2])
            keys.append((row[0],row[1]))
            target_result.append(float(row[2]))
    return keys, target_result


def add_hypernyms_to_dict(syn, level, dict):
    for hyp in syn.hypernyms():
        if not hyp in dict:
            dict[hyp] =level
        add_hypernyms_to_dict(hyp, level+1, dict)


## Date due dictonary { synset: livello profondità} estrae il synset comune con livello minore
def extract_common_hypernyms(dict1, dict2):
    min_hyp = None
    min_level = 99999
    for hyp in dict2.keys():
        if hyp in dict1:
            if min_level > dict1[hyp]:
                min_hyp = hyp
                min_level = dict1[hyp]
    return min_hyp


def lowes_common_subsumer(w1_syn, w2_syn):
    dict1 = {}
    dict2 = {}
    add_hypernyms_to_dict(w1_syn, 0, dict1)
    add_hypernyms_to_dict(w2_syn, 0, dict2)
    return extract_common_hypernyms(dict1, dict2)


def depth(syn):
    return 0 if not syn.hypernyms() else  1 + min(depth(hyp) for hyp in syn.hypernyms())


def max_depth():
    return 20
    #return max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wn.all_synsets())


def len_distance(syn1, syn2):
    dict1 = {}
    dict2 = {}
    if syn1 == syn2:
        return 0
    dict1[syn1] = 0
    dict2[syn2] = 0
    add_hypernyms_to_dict(syn1, 1, dict1)
    add_hypernyms_to_dict(syn2, 1, dict2)
    l = set(dict1.keys()).intersection(dict2.keys())
    return min([dict1.get(elem) + dict2.get(elem) for elem in l]) if l else max_depth()


def wup_similarity2(syn1, syn2):
    if lowes_common_subsumer(syn1, syn2) is None:
        return 0
    return 2 * depth(lowes_common_subsumer(syn1, syn2)) / (depth(syn1) +  depth(syn2))


def wup_similarity(syn1, syn2):
    if lowes_common_subsumer(syn1, syn2) is None:
        return 0
    subsumer = lowes_common_subsumer(syn1, syn2)
    depth_subsumer = depth(subsumer) + 1
    depth_syn1 = len_distance(syn1, subsumer) + depth_subsumer
    depth_syn2 = len_distance(syn2, subsumer) + depth_subsumer
    return 2 * depth_subsumer / (depth_syn1 + depth_syn2)


def path_similarity(syn1, syn2):
    return 2* max_depth() - len_distance(syn1, syn2)


def lch_similarity(syn1, syn2):
    #return -math.log(len_distance(syn1, syn2)/(2*max_depth()))
    return -math.log((len_distance(syn1, syn2)+1)/(2*19))


def wu_palmer(word1, word2):
    max = 0
    for w1_syn in wn.synsets(word1):
        for w2_syn in wn.synsets(word2):
            res = wup_similarity(w1_syn, w2_syn)
            max = res if res > max else max
    return max


def shortest_path(word1, word2):
    max = 0
    for w1_syn in wn.synsets(word1):
        for w2_syn in wn.synsets(word2):
            res = path_similarity(w1_syn, w2_syn)
            max = res if res > max else max
    return max


def leakcock_chodorow(word1, word2):
    max = 0
    for w1_syn in wn.synsets(word1):
        for w2_syn in wn.synsets(word2):
            res = lch_similarity(w1_syn, w2_syn)
            max = res if res > max else max
    return max

def calculate_similarity(list_keys):
    wu_palmer_result = []
    shortest_path_result = []
    leakcock_chodorow_result= []
    for key in list_keys:
        wu_palmer_result.append(wu_palmer(key[0],key[1]))
        shortest_path_result.append(shortest_path(key[0],key[1]))
        leakcock_chodorow_result.append(leakcock_chodorow(key[0],key[1]))
    return wu_palmer_result, shortest_path_result, leakcock_chodorow_result



if __name__ == "__main__":

    list, target_result = read_csv('WordSim353.csv')
    wu_palmer_result, shortest_path_result, leakcock_chodorow_result = calculate_similarity(list)

    print("WU PALMER RESULT:")
    print(scipy.stats.pearsonr(wu_palmer_result, target_result))
    print(scipy.stats.spearmanr(wu_palmer_result, target_result))

    print("Shortest Path:")
    print(scipy.stats.pearsonr(shortest_path_result, target_result))
    print(scipy.stats.spearmanr(shortest_path_result, target_result))

    print("Leakcock Chodorow RESULT:")
    print(scipy.stats.pearsonr(leakcock_chodorow_result, target_result))
    print(scipy.stats.spearmanr(leakcock_chodorow_result, target_result))

