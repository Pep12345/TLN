import numpy as np


class CkyNode:

    def __init__(self, value, x, y, leftNode=None, rightNode=None, word=None):
        self.value = value
        self.leftNode = leftNode
        self.rightNode = rightNode
        self.x = x
        self.y = y
        self.word = word

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    def getPosition(self):
        return '[' + str(self.x) + ',' + str(self.y) + ']'

    def print_w_par(self):
        if self.word is None:
            return self.value + self.getPosition()
        else:
            return self.value + self.getPosition() + ' ' + self.word


class Cell:

    def __init__(self, grammar, x, y):
        self.node_array = []
        self.grammar = grammar
        self.x = x
        self.y = y

    def __str__(self):
        return self.node_array.__str__() #if self.node_array.__len__() > 0 else ''

    def __repr__(self):
        return str(self)

    def add_word(self, word):
        for tag in self.grammar.get_rules_for_word(word):
            self.node_array.append(CkyNode(tag, self.x, self.y, word=word))

    def add_tag(self, cell_left, cell_right):
        for cky_node_left in cell_left.node_array:
            for cky_node_right in cell_right.node_array:
                tag_combination = cky_node_left.value + ' ' + cky_node_right.value
                for result_tag in self.grammar.get_rules_for_tag(tag_combination):
                    cky_node = CkyNode(result_tag, self.x, self.y, cky_node_left, cky_node_right)
                    self.node_array.append(cky_node)


def cky_parse(sentence, gr):
    words = sentence.split()
    table = np.empty((words.__len__(), words.__len__()+1), dtype=Cell)
    for j in range(1, words.__len__()+1):
        table[j-1][j] = Cell(gr, j-1, j)
        table[j-1][j].add_word(words[j-1])
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                if table[i, j] is None:
                    table[i, j] = Cell(gr, i, j)
                table[i, j].add_tag(table[i,k], table[k,j])
    return table
