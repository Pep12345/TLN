import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pprint import pprint
nasari = './utils/NASARI_vectors/dd-small-nasari-15.txt'

andy_text = './utils/docs/Andy-Warhol.txt'
ebola_text = './utils/docs/Ebola-virus-disease.txt'
life_text = './utils/docs/Life-indoors.txt'
napoleon_text = './utils/docs/Napoleon-wiki.txt'
trump_text = './utils/docs/Trump-wall.txt'
texts = [andy_text, ebola_text, life_text, napoleon_text, trump_text]

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def load_nasari_vectors(file):
    nasari_vct = []
    with open(file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            synsets = [w.split('_') for w in row[2:]]
            nasari_vct.append({'bn_id':row[0],
                                'wp_title':row[1],
                                'synsets':synsets})
    return nasari_vct


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


# Data una frase ritorna l'elenco dei lemmi filtrando le stop_words
def pre_processing(text):
    word_tokens = word_tokenize(text)
    return [lemmatizer.lemmatize(word) for word in word_tokens if not word.lower() in stop_words]


if __name__ == "__main__":
    for f in texts:
        title, paragraphs = read_doc(f)