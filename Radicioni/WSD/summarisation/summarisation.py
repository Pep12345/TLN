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

# Il corpus intero di nasari è troppo pesante per il mio povero pc, son stati aggiunte le righe relative
# ai babelnet id estratti da bebelfy usando solo il titolo dei documenti
nasari = './utils/NASARI_vectors/dd-small-nasari-15.txt'
#nasari_big = './utils/NASARI_vectors/dd-nasari.txt'

andy_text = './utils/docs/Andy-Warhol.txt'
ebola_text = './utils/docs/Ebola-virus-disease.txt'
life_text = './utils/docs/Life-indoors.txt'
napoleon_text = './utils/docs/Napoleon-wiki.txt'
trump_text = './utils/docs/Trump-wall.txt'
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


def get_paragraphs_score(paragraphs, topic, context, nasari_vct):
    paragraphs_score = []
    for i, p in paragraphs:
        word_list = pre_processing(p)
        bbn_ids_for_paragraphs = set(get_bbn_ids(' '.join(word_list)))
        nsr_vct_p = extract_nasari_from_babelnet_id(bbn_ids_for_paragraphs, nasari_vct)
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
        title, paragraphs, full_text = read_doc(f)

        # Estraggo il topic usando le parole del titolo + le 50 parole più frequenti
        try:
            bag_of_words = set(pre_processing(title) + bag_of_words(paragraphs, 10))
        except TypeError:
            print(bag_of_words(paragraphs, 10))
            exit()
        # Ottendo gli id di Babelnet dalle parole usando la risorsa di babelfy per disambiguare
        bbn_ids = set(get_bbn_ids(' '.join(bag_of_words)))

        # Estraggo il contesto dalle parole del topic
        topic = extract_nasari_from_babelnet_id(bbn_ids, nasari_vct)

        # Espando il contesto andando a cercare per ogni topic i nasari vector dei suoi lemmi
        context = []
        for v in topic:
            bbn_ids_for_topic = set(get_bbn_ids(' '.join(v.lemmas())))
            context += extract_nasari_from_babelnet_id(bbn_ids_for_topic, nasari_vct)

        #pprint(context)
        paragraphs_score = get_paragraphs_score(paragraphs, topic, context, nasari_vct)

        retrived_doc = my_summarize(paragraphs_score, paragraphs, 10)
        relevent_doc = summarize(full_text, 0.9)

        evaluation.print_result(title, relevent_doc, retrived_doc, full_text)
