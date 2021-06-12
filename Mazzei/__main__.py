from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from Cky import *
from grammar import Grammar
from tabulate import tabulate
from PyQt5.QtWidgets import QTreeWidgetItem
import sys


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data, words):
        super(TableModel, self).__init__()
        self._data = data
        self.words = ["0"]+[str(word) for word in words]


    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return str(self._data[index.row()][index.column()]) if self._data[index.row()][index.column()] is not None else self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self.words[section]
            if orientation == QtCore.Qt.Vertical:
                return ["0","1","2","3","4","5","6","7","8"][section]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, data, words):
        super().__init__()

        self.table = QtWidgets.QTableView()
        self.model = TableModel(data, words)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        self.setCentralWidget(self.table)


class TreeWindow(QtWidgets.QMainWindow):
    def __init__(self, table):
        super().__init__()

        self.tree = QtWidgets.QTreeWidget(self)
        list_s = []
        i = 1
        for elem in table[0, table[0].__len__() - 1].node_array:
            if elem.value == 'S':
                this_node = QTreeWidgetItem([str(elem.value)+elem.getPosition()])
                i += 1
                self.add_child(this_node, elem)
                list_s.append(this_node)

        for s in list_s:
            self.tree.addTopLevelItem(s)
        self.tree.resize(700, 500)
        self.tree.setHeaderLabels(["", ""])

    def add_child(self, tree_node, cky_node):
        if cky_node.leftNode is not None:
            left_node = QTreeWidgetItem(['Left', str(cky_node.leftNode)+cky_node.leftNode.getPosition()])
            self.add_child(left_node, cky_node.leftNode)
            tree_node.addChild(left_node)
        if cky_node.rightNode is not None:
            right_node = QTreeWidgetItem(['Right', str(cky_node.rightNode)+cky_node.rightNode.getPosition()])
            self.add_child(right_node, cky_node.rightNode)
            tree_node.addChild(right_node)


def convert_in_cf(grammar):
    return
    ## start-aggiungere simbolo iniziale s0
    ## term-eliminare i terminali dalle regole e mettere nuovi simboli non terminali
    # bin-eliminare regole con + di 2 a destra
    # del-eliminare epsilon-produzione:
    ## unit-eliminare regole unarie
    ##


def print_tree(table):
    string = ""
    for elem in table[0, table[0].__len__() - 1].node_array:
        if elem.value == 'S':
            string += "("+ elem.print_w_par() + add_child_string(elem) + ")"
    print(string)

def add_child_string(cky_node):
    string = ""
    if cky_node.leftNode is not None:
        string += "(" + cky_node.leftNode.print_w_par() + add_child_string(cky_node.leftNode) + ")"
    if cky_node.rightNode is not None:
        string += "(" + cky_node.rightNode.print_w_par() + add_child_string(cky_node.rightNode) + ")"
    return string


if __name__ == "__main__":
    # english
    #sentence = "Book the flight through Houston"
    #sentence = "Does she prefer a morning flight"
    #data = cky_parse(sentence, Grammar('L1_grammar_CF.txt'))

    # dothraki
    #sentence = 'Anha zhilak yera'
    #sentence = 'Anha gavork'
    sentence = 'Hash yer astoe ki Dothraki'
    data = cky_parse(sentence, Grammar('dothraki_grammar_CF.txt'))

    print(tabulate(data, sentence.split(), tablefmt="grid"))
    print_tree(data)

    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow(data, sentence.split())
    window.show()
    window.resize(400,200)

    tree_window = TreeWindow(data)
    tree_window.show()
    tree_window.resize(700,500)

    sys.exit(app.exec_())

