import csv
from utils import max_cos_sim
from utils import write_output_file
import utils
from utils import get_terms_from_synset
from pprint import pprint


# Leggo il file tsv con i valori attesi e memorizzo in dictionary:
# (word1,word2) -> [synset1, synset2, termini syn1, termini syn2]
def read_tsv(file_name):
    words_map = {} # (word1, word2) -> number
    with open('./' + file_name, "r", encoding='utf-8') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        for row in tsv_reader:
            key = (row[0], row[1])
            words_map[key] = ExpectedResults(sns_1=row[2], sns_2=row[3], terms_sns_1=row[4], terms_sns_2=row[5])
    return words_map


def main():
    # INIT FILE
    expected_result = read_tsv('/utils/si.test.data.expected.tsv')

    #INIT NASARI
    utils.set_nsr_dict()

    # INIT BABELNET
    utils.set_babelnet_api(expected_result)

    # variabili per risultati
    result = []
    number_of_correct = 0
    total_comparisson = 0

    # per ogni coppia di termini da classificare
    for w1, w2 in expected_result.keys():

        # estraggo i synset in base alla cosine similarity massima
        predicted_sns_1, predicted_sns_2 = max_cos_sim(w1, w2, return_type='arg')

        # salvo risultati in array per semplificare scrittura su file
        # memorizzo riga 1: valore atteso, riga 2: valore predetto
        exp_res = expected_result.get((w1, w2)) # risultato atteso
        result.append([w1, w2, exp_res.sns_1(), exp_res.sns_2(), exp_res.terms_1(), exp_res.terms_2()])
        result.append([w1, w2, predicted_sns_1, predicted_sns_2, get_terms_from_synset(predicted_sns_1), get_terms_from_synset(predicted_sns_2)])


        # statistiche: considero solo i casi in cui troviamo il vettore di nasari
        # l'accuratezza è calcolata sui singoli synset da identificare non sulla coppia
        if predicted_sns_1 is not None:
            if predicted_sns_1 == exp_res.sns_1():
                number_of_correct += 1
            if predicted_sns_2 == exp_res.sns_2():
                number_of_correct += 1
            if predicted_sns_1 != exp_res.sns_1() or predicted_sns_2 != exp_res.sns_2():
                print("Nuovo risultato mal identificato:")
                print("Atteso:", result[-2])
                print("Predetto:", result[-1])
                print("\n")
            total_comparisson += 2


    # salvo risultati su file
    write_output_file(result, path_file="utils/result_identification.tsv",
                      header="Row1:expected\nRow2:predicted\nword1,word2,bn_synset1,"
                             "bn_synset2,terms_bn_synset1,terms_bn_synset2")

    # stampo accuratezza
    print(f"Identificati correttamente {number_of_correct} su un totale di {total_comparisson}")
    print("Accuratezza: ", number_of_correct/total_comparisson)


class ExpectedResults:

    def __init__(self, sns_1, sns_2, terms_sns_1, terms_sns_2):
        self.__sns_1 = sns_1
        self.__sns_2 = sns_2
        self.__terms_sns_1 = terms_sns_1
        self.__terms_sns_2 = terms_sns_2

    def sns_1(self):
        return self.__sns_1

    def sns_2(self):
        return self.__sns_2

    def terms_1(self):
        return self.__terms_sns_1

    def terms_2(self):
        return self.__terms_sns_2

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'<<ExpectedResult> Synset word 1: {self.sns_1()}\t Synset word 2: {self.sns_2()}\t' \
               f' terms word 1: {self.terms_1()}\t terms word 2: {self.terms_2()} >'


if __name__ == "__main__":
    main()