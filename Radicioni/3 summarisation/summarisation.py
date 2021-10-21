import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nasari import load_nasari_vectors
from nasari import similarity
from babelfy import get_bbn_ids
import math
import evaluation

from gensim.summarization.summarizer import summarize

# Il corpus intero di nasari è troppo pesante per il mio pc, son stati aggiunte le righe relative
# ai babelnet id estratti da bebelfy usando solo il titolo dei documenti
nasari = './utils/NASARI_vectors/dd-small-nasari-15.txt'
#nasari_big = './utils/NASARI_vectors/dd-nasari.txt'

file_path = './utils/docs/'
andy_text = 'Andy-Warhol'
ebola_text = 'Ebola-virus-disease'
life_text = 'Life-indoors'
napoleon_text = 'Napoleon-wiki'
trump_text = 'Trump-wall'
texts = [andy_text, ebola_text, life_text, napoleon_text, trump_text]

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()


# Dato un articolo ne estraggo il titolo e una lista di coppie (numero paragrafo, testo)
def read_doc(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        # Extract title
        title_found = False
        while not title_found:
            line = f.readline().rstrip()
            if line and line[0] != '#':
                title = line
                title_found = True
        # Extract parapgraphs
        text = f.read().rstrip().replace('\n', '')
        paragraphs = []
        i = 0
        for sent in nltk.sent_tokenize(text):
            if len(sent) > 1:
                paragraphs.append((i, sent.rstrip()))
                i += 1
        return title, paragraphs, text


# Crea una bag of words con le K parole più frequenti data una lista di frasi
def bag_of_words(sent_list, number_of_words):
    words_counter = Counter()
    for sent in sent_list:
        words_counter.update(Counter(pre_processing(sent[1])))
    return [w[0] for w in words_counter.most_common(number_of_words)]


# Data una frase ritorna l'elenco dei lemmi filtrando le stop_words
def pre_processing(text):
    word_tokens = word_tokenize(text)
    return [lemmatizer.lemmatize(word) for word in word_tokens if not word.lower() in stop_words
                                                                    and word.isalnum()]


# Estraggo i vettori di nasari associati ad un babelnet ids contenuto in bbn_ids
def extract_nasari_from_babelnet_id(bbn_ids, nasari_vct):
    context = []
    for vct in nasari_vct:
        if vct.id() in bbn_ids and vct not in context:
            context.append(vct)
    return context


# Per lo score calcolo la similarità prima sul topic e poi sul contesto, dimezzando il peso del secondo
# e normalizzando il risultato
def get_paragraphs_score(paragraphs, topic, context, nasari_vct):
    paragraphs_score = []
    for i, p in paragraphs:
        # Cerco vettori nasari per il paragrafo
        word_list = pre_processing(p)
        bbn_ids_for_paragraphs = set(get_bbn_ids(' '.join(word_list)))
        nsr_vct_p = extract_nasari_from_babelnet_id(bbn_ids_for_paragraphs, nasari_vct)
        # Calcolo similarità
        sim = (similarity(topic, nsr_vct_p) + 0.5*similarity(context, nsr_vct_p)) / 1.5
        paragraphs_score.append((i, sim))
    return paragraphs_score


def my_summarize(paragraphs_score, paragraphs, cut_ratio):
    paragraphs_score = sorted(paragraphs_score, key=lambda tup: tup[1])
    number_of_paragraphs_to_remove = len(paragraphs) - math.floor(len(paragraphs) * (100 - cut_ratio) / 100)
    retrieved_doc = ''
    relevant_paragraph_ids = set([p[0] for p in paragraphs_score[number_of_paragraphs_to_remove:]])
    for p in paragraphs:
        if p[0] in relevant_paragraph_ids:
            retrieved_doc += ' \n ' + p[1]
    return retrieved_doc


if __name__ == "__main__":
    nasari_vct = load_nasari_vectors(nasari)

    for f in texts:
        title, paragraphs, full_text = read_doc(f'{file_path}{f}.txt')

        # Estraggo il topic usando le parole del titolo + le N parole più frequenti
        bag_of_words_result = set(pre_processing(title) + bag_of_words(paragraphs, 10))

        # Ottendo gli id di Babelnet dalle parole usando la risorsa di babelfy per disambiguare
        # Nota: questa risorsa utilizza una key concessa su iscrizione, si è limitati sul numero di richieste giornaliere
        bbn_ids = set(get_bbn_ids(' '.join(bag_of_words_result)))

        # Estraggo il contesto dalle parole del topic
        topic = extract_nasari_from_babelnet_id(bbn_ids, nasari_vct)

        # Espando il contesto andando a cercare per ogni topic i nasari vector dei suoi lemmi (usando babelfy)
        context = []
        for v in topic:
            bbn_ids_for_topic = set(get_bbn_ids(' '.join(v.lemmas())))
            context += extract_nasari_from_babelnet_id(bbn_ids_for_topic, nasari_vct)

        # Estraggo gli score usando WO
        paragraphs_score = get_paragraphs_score(paragraphs, topic, context, nasari_vct)

        # Calcolo il file finale risultante applicando una riduzione del _cut_ratio%
        _cut_ratio = 30
        retrived_doc = my_summarize(paragraphs_score, paragraphs, _cut_ratio)
        # Creo file di confronto usando le librerie gensim
        relevent_doc = summarize(full_text, (100-_cut_ratio)/100)

        # Stampo risultati
        evaluation.print_result(title, f, relevent_doc, retrived_doc, full_text)


'''
output:
TITLE:   Andy Warhol: Why the great Pop artist thought ‘Trump is sort of cheap’
PRECISION:  0.7619047619047619
RECALL:  0.8

TITLE:   Ebola virus disease
PRECISION:  0.7540983606557377
RECALL:  0.7540983606557377

TITLE:   How people around the world are coping with life indoors
PRECISION:  0.7857142857142857
RECALL:  0.7857142857142857

TITLE:   Napoleone Bonaparte.
PRECISION:  0.75
RECALL:  0.75

TITLE:   The Trump wall, commonly referred to as "The Wall", was an expansion of the Mexico–United States barrier during the U.S. presidency of Donald Trump. Throughout his 2016 presidential campaign, Trump called for the construction of a border wall. He said that, if elected, he would "build the wall and make Mexico pay for it". Then-Mexican president Enrique Peña Nieto said that Mexico would not pay for the wall.
PRECISION:  0.7971014492753623
RECALL:  0.7857142857142857
'''