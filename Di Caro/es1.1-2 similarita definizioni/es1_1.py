import csv
import os
import pprint
import numpy
import warnings
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances


def read_csv(file_name):
    meanings_map = {}
    dir = os.path.dirname(os.path.abspath(__file__))
    with open(dir + '/' + file_name, "r") as csv_file:
        words = csv_file.readline().replace('\n','').split(',')
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            for i in range(1, 5):
                if not meanings_map.keys().__contains__(words[i]):
                    meanings_map[words[i]] = []
                meanings_map[words[i]].append(row[i]) if len(row[i]) > 0 else None
    return meanings_map


def preprocessing(meanings_map):
    ps = PorterStemmer()
    for key in meanings_map:
        for definition in meanings_map.get(key):
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(definition)
            filtered_sentence = [ps.stem(w.lower()) for w in word_tokens if not w.lower() in stop_words and w.lower().isalnum()]
            meanings_map.get(key)[meanings_map.get(key).index(definition)] = filtered_sentence


def print_result(word, intersection_list, similarity, percentage=False):
    print(f"Result for term: {word}")
    print(f"Percentage used for filtering: {percentage}") if percentage else None
    print(f"Intersection list: {intersection_list}")
    print(f"Similarity: {similarity}")
    print("\n\n")


def calculate_normal_similarity(meanings_map):
    for word in meanings_map:
        definition_lists = meanings_map.get(word)
        sum_len = 0
        intersection_list = definition_lists[0]
        for definition in definition_lists:
            intersection_list = [word for word in intersection_list if word in set(definition)]
            sum_len += definition.__len__()
        similarity = len(intersection_list) / ( sum_len / len(definition_lists))
        print_result(word, intersection_list, similarity)


def calculate_percentage_similarity(meanings_map, percentage):
    for word in meanings_map:
        definition_lists = meanings_map.get(word)
        word_counter = Counter(x for xs in definition_lists for x in set(xs))
        intersection_list = [word for word in word_counter.keys() if word_counter.get(word)/len(definition_lists) > percentage]
        sum_len = sum(len(x) for x in definition_lists)
        similarity = len(intersection_list) / (sum_len / len(definition_lists))
        print_result(word, intersection_list, similarity, percentage)


def get_mean_diagonal_matrix(matrix):
    list_term = []
    for i in range(0, len(matrix)):
        list_term = numpy.append(list_term, matrix[i][i+1:len(matrix)])
    return sum(list_term) / len(list_term)


def get_cosine_sim(meanings_map):
    for word in meanings_map:
        input_list = [' '.join(definition) for definition in meanings_map.get(word)]
        vectors = [t for t in get_vectors(input_list)]
        print(word)
        res = cosine_similarity(vectors)
        print_result(word, None, get_mean_diagonal_matrix(res))



def get_vectors(text):
    # Son presenti dei warning di tipo FutureWarning:
    # From version 1.0 (renaming of 0.25) passing these as positional arguments will result in an error
    # per agevolare la lettura li filtriamo
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        vectorizer = CountVectorizer(text)
        vectorizer.fit(text)
    return vectorizer.transform(text).toarray()


if __name__ == "__main__":
    meanings_map = read_csv('defs.csv')
    # For each definition ->
    #       create a list of words filtering punctuation, stop words and appling stemmatization and lowercase
    preprocessing(meanings_map)
    get_cosine_sim(meanings_map)
    #calculate_normal_similarity(meanings_map)
    #calculate_percentage_similarity(meanings_map, 0.5)
    #get_cosine_sim(meanings_map)
    #pprint.pprint(meanings_map['Paper'])

