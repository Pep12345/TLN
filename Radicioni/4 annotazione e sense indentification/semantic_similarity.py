#Biondi         :	coppie nell'intervallo 251-300
import os
import csv
import nasari
import utils
import scipy.stats
from utils import max_cos_sim
from utils import write_output_file


# Leggo il file tsv con i valori attesi e memorizzo in dictionary:
# (word1,word2) -> valore
def read_tsv(file_name):
    words_map = {} # (word1, word2) -> number
    with open('./' + file_name, "r", encoding='utf-8') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        for row in tsv_reader:
            key = (row[0],row[1])
            value = int(row[2])
            words_map[key] = value
    return words_map


# metodo per convertire i risultati della cos_similarity in valori di range 0-4
def convert_0_1_range_to_0_4_range(old_value):
    #(((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
    # nel caso non sia stato trovato nessun valore di similarità
    if old_value == -1:
        return old_value
    return (((old_value - 0) * (4-0)) / (1 - 0)) + 0


if __name__ == "__main__":

    # INIT FILE
    expected_result = read_tsv('/utils/it.test.data.expected.tsv')

    #INIT NASARI
    utils.set_nsr_dict()

    # INIT BABELNET
    utils.set_babelnet_api(expected_result)

    # variabili per risultati
    result = []
    _my_result = []
    _cos_sim_result = []

    # per ogni coppia di termini da classificare
    for w1, w2 in expected_result.keys():

        # calcolo la max similarity e la converto in range 0-4
        max_sim = convert_0_1_range_to_0_4_range(max_cos_sim(w1, w2))

        # salvo risultati in array per semplificare scrittura su file
        result.append([w1, w2, expected_result.get((w1, w2)), max_sim])

        # statistiche: considero solo i casi in cui troviamo il vettore di nasari
        if max_sim != -1:
            _my_result.append(expected_result.get((w1, w2)))
            _cos_sim_result.append(max_sim)

    # salvo risultati su file
    write_output_file(result, path_file="utils/result_valutation.tsv",
                      header="word1,word2,my_score,cos_similarity")

    # stampo statistiche
    print("Pearson: ", scipy.stats.pearsonr(_my_result, _cos_sim_result)[0])
    print("Spearman: ", scipy.stats.spearmanr(_my_result, _cos_sim_result)[0])

'''
Pearson:  0.6004152835410147
Spearman:  0.6006212225067805
'''






