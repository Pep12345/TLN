from nltk import load_parser
import os

dir = os.path.dirname(os.path.abspath(__file__))
text_file = 'file://' + dir + '/dothraki_gr_sem.fcfg'
parser = load_parser(text_file, trace=0)
sentence = 'Anha zhilak yera'
sentence2 = 'Anha gavork'
sentence3 = 'Hash yer astoe ki Dothraki'
tokens = sentence.split()
for tree in parser.parse(tokens):
    print("Label: "+str(tree.label()['SEM'])+"\n")
    print(tree)
