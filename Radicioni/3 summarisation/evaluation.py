import difflib
import nltk
from pprint import pprint
import os
from nltk.tokenize import sent_tokenize

output_dictory = './docs/result'


# Stampa le frasi che text2 ha in meno rispetto text1
def difference(text1, text2):
    s1 = set([s.strip() for s in sent_tokenize(text1)])
    s2 = set([s.strip() for s in sent_tokenize(text2)])
    return '\n'.join(list(s1.difference(s2)))


def print_difference(relevant_doc, retrived_doc, original_text):
    return "sentence removed:\n" + difference(original_text, retrived_doc) \
           + "\n\n\nsentence removed expected:\n" + difference(original_text, relevant_doc)


def precision(relevant_doc, retrieved_doc):
    rel_d = set(nltk.sent_tokenize(relevant_doc))
    ret_d = set(nltk.sent_tokenize(retrieved_doc))
    return len(rel_d.intersection(ret_d))/len(ret_d)


def recall(relevant_doc, retrieved_doc):
    rel_d = set(nltk.sent_tokenize(relevant_doc))
    ret_d = set(nltk.sent_tokenize(retrieved_doc))
    return len(rel_d.intersection(ret_d))/len(rel_d)


### METODI PER CREARE FILE OUTPUT ###
def create_dir(title):
    _new_dir = output_dictory+'/'+title
    if not os.path.exists(_new_dir):
        os.makedirs(_new_dir)
    return _new_dir


def print_file(title, file_text, path):
    f = open(f'{path}/{title}.txt', 'w+')
    f.write(file_text)
    f.close()


def make_output_file(title, relevant_doc, retrived_doc, difference):
    path = create_dir(title)
    # file gold
    print_file('gold', relevant_doc, path)
    # file ottenuto
    print_file('my_result', retrived_doc, path)
    # difference
    print_file('difference', difference, path)


def print_result(title, file_name, relevant_doc, retrived_doc, original_text):
    print("TITLE:  ",title)
    print("PRECISION: ", precision(relevant_doc, retrived_doc))
    print("RECALL: ", recall(relevant_doc, retrived_doc))
    _difference = print_difference(relevant_doc, retrived_doc, original_text)
    print(_difference)
    make_output_file(file_name, relevant_doc, retrived_doc, _difference)
    print('\n\n\n')
