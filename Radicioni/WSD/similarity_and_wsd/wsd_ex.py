from nltk.corpus.reader import semcor
from nltk.corpus import semcor
from nltk.corpus import wordnet as wn
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus.reader.wordnet import WordNetError
import os, random
import nltk


'''
    Domande:
        1) Come gestire le parole con _: 1) nella funzione randomica metto un controllo che la parola estratta non lo abbia
                                         2) passo il lemma del corpus invece della parola
        2) dovrei cercare il lemma su wordnet o la parola base?
        3) nel corpus esistono key che non son presenti su wordnet (es. recent frase 1)
        4) nel overlap usare lemma o stemma per confronto?
        
        Usare lemma invece della parola perchè spesso escono termini con _
'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ERROR = "\033[31m"


stop_words = set()
print_on_off = False


def explaination_on():
    global print_on_off
    print_on_off = True


def explaination_off():
    global print_on_off
    print_on_off = False


def read_stop_words():
    global stop_words
    stop_words = set()
    dir = os.path.dirname(os.path.abspath(__file__))
    file_name = 'stop_words_FULL.txt'
    with open(dir + '/' + file_name, "r") as f:
        for line in f.read().splitlines():
            stop_words.add(line)
    return stop_words


# uso lemma per rimuovere le stop words
def extract_words_from_sentence(sentence):
    global stop_words
    if len(stop_words) ==0:
        read_stop_words()
    lemmatizer = WordNetLemmatizer()
    sents = nltk.sent_tokenize(sentence)
    sents = [s[0].lower() + s[1:] for s in sents]   # rimuovo la prima lettera maiuscola per non perdere nomi propri
    sentence = ' '.join(sents)
    return [word for word in nltk.tokenize.word_tokenize(sentence)
                if word.isalnum() and lemmatizer.lemmatize(word) not in stop_words]


def read_gloss_and_examples(syn):
    list_words = []
    new_list = syn.examples() + [syn.definition()]
    for sentence in new_list:
        list_words += extract_words_from_sentence(sentence)
    return list_words


def compute_overlap(signature, context):
    porter = PorterStemmer()
    #lemmatizer = WordNetLemmatizer()
    counter = 0
    for word in context:
        for sign in signature:
            if porter.stem(word.lower()) == porter.stem(sign.lower()):
            #if lemmatizer.lemmatize(word) == lemmatizer.lemmatize(sign):
                counter += 1
    return counter


def simplified_lesk(word, sentence):
    if len(wn.synsets(word)) == 0:
        return None
    else:
        best_sense = wn.synsets(word)[0]
    max_overlap = 0
    context = extract_words_from_sentence(sentence)
    if print_on_off: print("Context list: " + str(context))
    for sense in wn.synsets(word):
        signature = read_gloss_and_examples(sense)
        overlap = compute_overlap(signature, context)
        if print_on_off: print("Signature for synset:" + str(sense)+ " \nlist: " + str(signature)
                                                                +"\noverlap result: "+ str(overlap))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense
    return best_sense


# extraggo casualmente una parola che rispetti le condizioni
def get_random_word(list_words_for_sentence):
    found = True
    while found:
        index = random.randint(0, len(list_words_for_sentence) - 1)
        word = list_words_for_sentence[index]
        if word.tag == "wf" and word.attrib["cmd"] == "done" and "ot" not in word.attrib.keys():
                                                                    # and '_' not in set(word.text):
            found = False
    return word


def execute_test(list_words_for_sentence):

    full_sentence = ' '.join(word.text for word in list_words_for_sentence).replace('_', ' ')
    word = get_random_word(list_words_for_sentence)

    print("Extracted word:  ", word.text)
    print("Sentence for test:  ", full_sentence)
    lemma = word.attrib["lemma"] + '%' + word.attrib['lexsn']
    try:
        expected_synset = wn.lemma_from_key(lemma).synset()
    except WordNetError as e:
        print(f"{bcolors.ERROR}Impossible calculate cause: {e}{bcolors.ENDC}")
        print("Return False")
        return False

    calculated_synset = simplified_lesk(word.text, full_sentence)
                        # simplified_lesk(word.attrib["lemma"], full_sentence)

    print("Algorithm result: ", calculated_synset)
    print("Expected result: ", expected_synset)

    return expected_synset == calculated_synset if calculated_synset is not None else False



if __name__ == "__main__":
    read_stop_words()
    file_name = '/brown1/tagfiles/br-a01.xml'
    k = 50 # indice per il numero di iterazioni

    # questo comando attiva le stampe delle bag words usate negli overlap
    #explaination_on()

    list_of_sentences = semcor.xml(file_name).findall('context/p/s')
    correct_result = 0
    print("Starting test...\n")

    for i in range(0, k):
        print("Iteration number ", i)
        sentence_index = random.randint(0, len(list_of_sentences) - 1)
        result = execute_test(list_of_sentences[sentence_index])
        print("\n\n")
        if result:
            correct_result += 1

    print("Correct result: ", correct_result)
    print("Number of execution: ", k)
    print("Precision: ", correct_result / k)
