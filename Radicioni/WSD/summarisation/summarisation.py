
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pprint import pprint
from collections import Counter
from nasari import load_nasari_vectors
from nasari import wo

nasari = './utils/NASARI_vectors/dd-small-nasari-15.txt'

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
        while(not title_found):
            line = f.readline().rstrip()
            if line and line[0] != '#':
                title = line
                title_found = True
        # Extract parapgraphs
        paragraphs = []
        i = 0
        for sent in f:
            if len(sent) > 1:
                paragraphs.append((i, sent.rstrip()))
                i += 1
        return title, paragraphs


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

# Creo il contesto come la lista dei synset per ogni vettore
# che contiene nel titolo una parola delle bag of words
def extract_nasari_context(bag_of_words, nasari_vct):
    context = []
    for word in bag_of_words:
        for vct in nasari_vct:
            if word in vct.title().split('-'):
                if vct.syn_array() not in context:
                    context += vct.syn_array()
    return context


if __name__ == "__main__":
    nasari_vct = load_nasari_vectors(nasari)
    print(wo(nasari_vct[0], nasari_vct[4]))
    for f in texts:
        title, paragraphs = read_doc(f)

        # Estraggo il topic usando le parole del titolo + le 50 parole più frequenti
        topic = set(pre_processing(title) + bag_of_words(paragraphs, 50))

        # Estraggo il contesto dalle parole del topic
        context = extract_nasari_context(topic, nasari_vct)


        exit()
