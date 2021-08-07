from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import os
import nltk
import sys
sys.path.append('..')
from similarity_and_wsd import wsd_ex as wsd
from nltk.stem import PorterStemmer
from pprint import pprint
import json
import re



'''
    Domande:
        1) Nella costruzione del contesto FN dovrei usare anche le definizioni delle LU?
        2) Nella creazione delle bag of words, è corretto usare un set? Per es.
                A 'dog' 
                B 'dog', 'dog'
            Considera 1 overlap quando sarebbero 2
'''


'''
    student: Biondi
        ID:   44	frame: Volubility
        ID: 1812	frame: Coincidence
        ID: 1192	frame: Transfer_scenario
        ID: 1863	frame: Becoming_separated
        ID:  277	frame: Food
'''
list_input = ['Volubility', 'Coincidence', 'Transfer_scenario', 'Becoming_separated', 'Food']

### METODI PER FILE
# Creo file da annotare manualmente coi synset attesi
# Nota: per i termini composti 'Transfer_scenario' a mano verranno scelte le parole principali sul file
def create_valutation_file():
    v = {}
    for w in list_input:
        fe_expected_result_dictionary = { fe : "None" for fe in fn.frames(w)[0].FE}
        lu_expected_result_dictionary = { lu : "None" for lu in fn.frames(w)[0].lexUnit}
        v[w] = {'this': None, 'FE': fe_expected_result_dictionary,'LU': lu_expected_result_dictionary}
    with open('valutation_file.txt', 'w') as f:
        f.write(json.dumps(v, indent=4))


def read_valutation_file():
    with open('valutation_file.txt', 'r') as f:
        data = json.load(f)
    return data


def stemmer(list_of_words):
    porter = PorterStemmer()
    return [porter.stem(w) for w in list_of_words]


### METODI CONTEXT
# bow = bag of words
def get_wordnet_context_bow(synset):     ### Ctx(s)
    signature = wsd.read_gloss_and_examples(synset)
    for hyp in synset.hypernyms():
        signature += wsd.read_gloss_and_examples(hyp)
    for hyp1 in synset.hyponyms():
        signature += wsd.read_gloss_and_examples(hyp1)
    return stemmer(signature)


#def get_framenet_context_bow(frame_term):     ### Ctx(w)
    #frame = fn.frame(frame_term)
    #signature = wsd.extract_words_from_sentence(frame.definition)
    #for f in frame.FE:
    #    signature += wsd.extract_words_from_sentence(frame.FE[f].definition)
    #for lu in frame.lexUnit:           # dovrei usare anche la definizione delle lu?
        #signature += wsd.extract_words_from_sentence(frame.lexUnit[lu].definition)
    #return stemmer(signature)
def get_framenet_context_bow(frame_part):     ### Ctx(w)
    signature = wsd.extract_words_from_sentence(frame_part.definition)
    return stemmer(signature)



### METODI MAPPING SCORE
def bag_of_words_score(ctxw, synset):
    ctxs = get_wordnet_context_bow(synset)
    #ctxw = get_framenet_context_bow(frame)
    return len(set(ctxs).intersection(set(ctxw)))+1


def graphic_score(frame, synset):
    return


def extract_fn_wn_word(term):
    # per gestire le parole composte nel file scriveremo 'parola_composta[parola]' così da usare parola per wn
    if '[' in term:
        wordnet_word = re.search(r'(?<=\[).+?(?=\])', term).group()
        frame_word = re.search(r'.+?(?=\[)', term).group()
    else:
        frame_word = term
        wordnet_word = term
    return frame_word, wordnet_word


def get_best_synset(wordnet_word, frame_part, flag=0):
    if len(wn.synsets(wordnet_word)) == 0:
        return None

    framenet_ctxw = get_framenet_context_bow(frame_part)
    best_score = -1
    for synset in wn.synsets(wordnet_word):    ## dovrei mettere n per prendere solo noun?
        if flag == 0:
            score = bag_of_words_score(framenet_ctxw, synset)
        #else:
         #   score = graphic_score(frame,synset)
        if score > best_score:
            best_score = score
            best_sense = synset
    #print(word, ': ',best_sense, best_score)
    return best_sense


# Confronto gli ID, creato per leggibilità
def compare_syn(found_synset, expected_string):
    return wn.synset(expected_string).offset() == found_synset.offset()


def print_wrong_result(found, expected):
    print("Wrong result:\n\texpected: ", expected[0]," words: ", expected[1],
          "\n\tfound: ", found.name(), "words: ", found.lemma_names())

if __name__ == "__main__":
    #print(get_best_synset('Transfer_scenario[Transfer]'))
    #print(input.get('Volubility').get('FE').get('Speaker')[0] == str(wn.synset('speaker.n.1')))
    ###
    # wsd.read_stop_words()
   # frame = fn.frames(wn_input[1])[0]
   # synset = wn.synsets(wn_input[1])[0]
   # print(get_wordnet_context_bow(synset), get_framenet_context_bow(frame))
    #print(wsd.compute_overlap(get_wordnet_context_bow(synset), get_framenet_context_bow(frame)))
   # print(bag_of_words_score(frame, synset))
###
    # Carico le stop-words in memoria
    wsd.read_stop_words()
    # Carico Dictionary con gli elementi da cercare e i risultati attesi. Per info: valutation_file.txt
    input = read_valutation_file()
    result_counter = []
    
    for word in input.keys():
        # Inizializzo parametri
        correct, total = 0, 0

        # Estraggo frame
        frame_word, wordnet_word = extract_fn_wn_word(word) # Metodo per gestire parole composte
        frame = fn.frame(frame_word)
        
        # Estraggo best synset e confronto
        syn = get_best_synset(wordnet_word, frame)
        if compare_syn(syn, input[word]['this'][0]):
            correct += 1
        else:
            print_wrong_result(syn, input[word]['this'])
        total += 1

        # Ripeto per ogni FE
        fe_expected_result_dictionary = input[word]['FE']
        for fe in fe_expected_result_dictionary.keys():
            if fe_expected_result_dictionary.get(fe) == "None":
                print(correct)
                print(total)
                exit() #continue

            frame_word, wordnet_word = extract_fn_wn_word(fe)

            fe_syn = get_best_synset(wordnet_word, frame.FE[frame_word])
            if compare_syn(fe_syn, fe_expected_result_dictionary.get(fe)[0]):
                correct += 1
            else:
                print_wrong_result(fe_syn, fe_expected_result_dictionary.get(fe))
            total += 1

        
        # Ripeto per ogni LexUnits
        lu_expected_result_dictionary = input[word]['LU']
        for lu in lu_expected_result_dictionary.keys():

            frame_word, wordnet_word = extract_fn_wn_word(lu)
            # per rimuovere la parte sul tipo del lexunit es. 'effusive.a'
            if '.' in wordnet_word:
                wordnet_word = wordnet_word.split('.')[0]

            lu_syn = get_best_synset(wordnet_word, frame.lexUnit[frame_word])
            if compare_syn(lu_syn, lu_expected_result_dictionary.get(lu)[0]):
                correct += 1
            else:
                print_wrong_result(lu_syn, lu_expected_result_dictionary.get(lu))
            total += 1

        print(word, correct, total)
    exit()











    for lu in frame.lexUnit:
        print(frame.lexUnit[lu].definition)
        print(frame.lexUnit[lu].name)
    print(get_framenet_context_bow(frame))
    exit()
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
