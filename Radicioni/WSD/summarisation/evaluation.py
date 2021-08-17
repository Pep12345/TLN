import difflib
import nltk
from pprint import pprint


def difference(text1, text2):
    return ''.join([li[-1] for li in difflib.ndiff(text1, text2) if li[0] != ' '])


def precision(relevant_doc, retrieved_doc):
    rel_d = set(nltk.sent_tokenize(relevant_doc))
    ret_d = set(nltk.sent_tokenize(retrieved_doc))
    return len(rel_d.intersection(ret_d))/len(ret_d)


def recall(relevant_doc, retrieved_doc):
    rel_d = set(nltk.sent_tokenize(relevant_doc))
    ret_d = set(nltk.sent_tokenize(retrieved_doc))
    return len(rel_d.intersection(ret_d))/len(rel_d)


def print_result(title, relevant_doc, retrived_doc, original_text):
    print("TITLE:  ",title)
    print("PRECISION: ", precision(relevant_doc, retrived_doc))
    print("RECALL: ", recall(relevant_doc, retrived_doc))
    print("\nsentence removed: ")
    print(difference(original_text, retrived_doc))
    print("\nsentence removed expected: ")
    print(difference(original_text, relevant_doc))