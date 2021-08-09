import csv
from pprint import pprint
nasari = './utils/NASARI_vectors/dd-small-nasari-15.txt'

andy_text = './utils/docs/Andy-Warhol.txt'
ebola_text = './utils/docs/Ebola-virus-disease.txt'
life_text = './utils/docs/Life-indoors.txt'
napoleon_text = './utils/docs/Napoleon-wiki.txt'
trump_text = './utils/docs/Trump-wall.txt'
texts = [andy_text, ebola_text, life_text, napoleon_text, trump_text]


def load_nasari_vectors(file):
    nasari_vct = []
    with open(file, "r", encoding="utf-8") as csv_file:
        csv_file.readline()
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            synsets = [w.split('_') for w in row[2:]]
            nasari_vct.append({'bn_id':row[0],
                                'wp_title':row[1],
                                'synsets':synsets})
    return nasari_vct





if __name__ == "__main__":
    pprint(load_nasari_vectors(nasari))