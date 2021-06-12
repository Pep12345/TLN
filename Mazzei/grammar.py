import os
from collections import defaultdict

class Grammar:

    lexical_rules = defaultdict(set)
    syn_rules = defaultdict(set)   # non dovrebbe servire

    def __init__(self, text_file):
        dir = os.path.dirname(os.path.abspath(__file__))
        with open(dir + '/' + text_file, "r") as cfg:
            while cfg:
                line = cfg.readline()
                if line == "":
                    break
                line = line.replace('| ', '|').replace(' |', '|').replace('\n', '').split('->')
                for body in line[1].split('|'):
                    #self.rules.append({line[0]: body})
                    self.add_rule(line[0], body)

    def add_rule(self, head, body):
        if body[0] == '\'':
            self.lexical_rules[body.replace('\'','').lower()].add(head)
        else:
            self.syn_rules[body].add(head)


    #Get testa regola dato corpo
    def get_rules_for_word(self, word):
        return list(self.lexical_rules.get(word.lower()) if self.lexical_rules.__contains__(word.lower()) else [])
        #return [head for body, head in self.lexical_rules.items() if body.replace('\'','') == word]

    def get_rules_for_tag(self, tag):
        return list(self.syn_rules.get(tag) if self.syn_rules.__contains__(tag) else [])
        #[head for body,head in self.syn_rules.items() if body==tag]


    def print(self):
        print("Lexical ruels:")
        for k, v in self.lexical_rules.items():
            for v1 in v:
                print(v1+'->'+k)
        print("\n\nSyn rules")
        for k,v in self.syn_rules.items():
            for v1 in v:
                print(v1 + '->' + k)