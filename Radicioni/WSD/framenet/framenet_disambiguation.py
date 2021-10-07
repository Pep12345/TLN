from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from utils import read_valutation_file, extract_fn_wn_word
from pprint import pprint
from bag_of_words_alg import get_framenet_context_bow, get_wordnet_context_bow, wsd
from graph_score import probability, get_big_framenet_context_bow
'''
    student: Biondi
        ID:   44	frame: Volubility
        ID: 1812	frame: Coincidence
        ID: 1192	frame: Transfer_scenario
        ID: 1863	frame: Becoming_separated
        ID:  277	frame: Food
'''


# ctxw lo passo da fuori per non ricalcolarlo ad ogni iterazione
def bag_of_words_score(ctxw, synset):
    ctxs = get_wordnet_context_bow(synset)
    return len(set(ctxs).intersection(set(ctxw)))+1


def graphic_score(fn_ctxw, wn_word, sns, l):
    return probability(sns, wn_word, fn_ctxw, l)


# Estraggo il best synset in base al tipo di score, flag 0 per bag of words, flag != 0 per graph (TODO)
def get_best_synset(wordnet_word, frame_part, flag=0, pos=None):
    if len(wn.synsets(wordnet_word)) == 0:
        return None

    framenet_ctxw = get_framenet_context_bow(frame_part)
    framenet_ctxw_big = get_big_framenet_context_bow(frame.name)
    best_score = -1

    # nel caso delle lex_units sfruttiamo la conoscenza sul pos per ridurre i synset
    if pos:
        wn_sns = wn.synsets(wordnet_word, pos)
    else:
        wn_sns = wn.synsets(wordnet_word)

    for sns in wn_sns:
        if flag == 0:
            score = bag_of_words_score(framenet_ctxw_big, sns)
        else:
            score = graphic_score(framenet_ctxw, wordnet_word, sns, 4)

        if score > best_score:
            best_score = score
            best_sense = sns
    #print(word, ': ',best_sense, best_score)
    return best_sense


# Confronto gli ID
def compare_syn(found_synset, expected_string):
    return wn.synset(expected_string).offset() == found_synset.offset()


# stampo i risultati non uguali
def print_wrong_result(word, found, expected):
    print(f"Wrong result on word: {word}\n\texpected: ", expected[0]," terms: ", expected[1],
          "\n\tfound: ", found.name(), "terms: ", found.lemma_names(),"\n")


# estraggo dal frame l'elemento in base al tipo (main,fe,lu) e al termine
def extract_frame_syn(frame_word, type):
    global frame
    if type == 'MAIN':
        frame = fn.frame(frame_word)
        return frame
    if type == 'FE':
        return frame.FE[frame_word]
    if type == 'LU':
        return frame.lexUnit[frame_word]
    raise ValueError("frame type unknown")


# controllo se predizione ( best_syn) e atteso (expected_result) combaciano
# se si incremento variabili di score globali
def compare(word, expected_result, type):
    global correct, total
    if expected_result != "None":
        fn_word, wn_word = extract_fn_wn_word(word)

        # solo per lex units:
        # per rimuovere la parte sul tipo del lexunit es. 'effusive.a'
        pos = None
        if type == 'LU' and '.' in wn_word:
            split = wn_word.split('.')
            wn_word = split[0]
            pos = split[1]
            if pos == 'adv': pos = 'r'  # correzione per gli avverbi che han simboli diversi

        best_syn = get_best_synset(wn_word, extract_frame_syn(fn_word, type), flag=1, pos=pos)
        if compare_syn(best_syn, expected_result[0]):
            correct += 1
        else:
            print_wrong_result(word, best_syn, expected_result)
        total += 1


# per ogni fe/lu controllo se predizione e atteso son uguali
def compare_loop(frame_dict, category_type):
    if category_type not in {'FE','LU'}: raise ValueError('wrong type line 133')

    sub_dict = frame_dict[category_type]
    for key in sub_dict.keys():
        compare(key, sub_dict.get(key), type=category_type)


if __name__ == "__main__":

    # INIT STOP WORDS
    wsd.read_stop_words()

    # INIT EXPECTED RESULT
    input = read_valutation_file()

    result_counter = []  # salvo i risultati

    # Per ognuna delle 5 parole:
    for word in input.keys():

        print(f"Starting frame for word: {word}\n")
        # Inizializzo parametri score
        correct, total = 0, 0

        # controllo se predizione e atteso combaciano nel significato generale
        compare(word, input[word]['this'], type='MAIN')

        # Ripeto per ogni FE
        compare_loop(input[word], category_type='FE')

         # Ripeto per ogni LexUnits
        compare_loop(input[word], category_type='LU')

        # memorizzo risultati
        result_counter.append((word, correct, total))

    # stampo risultati
    for r in result_counter:
        print(f"Result for word: {r[0]}:")
        print(f"Correct predictions: {r[1]}")
        print(f"Total comparisons: {r[2]}")
        print(f"Score: {r[1]/r[2]}\n")
'''
bag of words
Volubility 27 34
Coincidence 7 14
Transfer_scenario[Transfer] 5 5
Becoming_separated[Becoming] 9 16
Food 62 75

graph
Volubility 24 34
Coincidence 9 14
Transfer_scenario[Transfer] 3 5
Becoming_separated[Becoming] 9 16
Food 51 75
'''