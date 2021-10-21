from py_babelnet.calls import BabelnetAPI


class BabelNetApi:

    key = '2e40ff40-ee1b-4a94-ba7e-66d30c616145'
    key2 = 'd65a7170-9d89-4703-ae2f-31dc31bdd24c'

    def __init__(self, list_words, n=1):
        if n == 1:
            self.__api = BabelnetAPI(self.key)
        else:
            self.__api = BabelnetAPI(self.key2)
        self.bn_dict = {}  # dict word -> bn.id
        self.sns_terms = {}  # dict bn.id -> information terms
        self.init_dict(list_words)

    def init_dict(self, list_words):
        for w in list_words:
            senses = self.__api.get_senses(lemma=w, searchLang="IT")
            for sense in senses:
                self.__add_sense_id(w, sense)  # add id in bn_dict
                self.__add_terms_to_synsets(sense)  # add terms in sns_terms

    # Per limitare il numero di chiamate estriamo tutte le info usando una sola chiamata
    # e memorizziamo le parti di interesse coi seguenti metodi:
    # memorizzo tutti i synset associati ad una data parola
    def __add_sense_id(self, word, sense):
        sense_ids = sense['properties']['synsetID']['id']
        if self.bn_dict.__contains__(word):
            self.bn_dict.get(word).add(sense_ids)
        else:
            self.bn_dict[word] = {sense_ids} # using set, not array

    # memorizzo tutti i termini usati come lemma di un dato synset
    def __add_terms_to_synsets(self, sense):
        sense_ids = sense['properties']['synsetID']['id']
        term = sense['properties']['simpleLemma'].lower()
        if self.sns_terms.__contains__(sense_ids):
            self.sns_terms.get(sense_ids).add(term)
        else:
            self.sns_terms[sense_ids] = {term}

    ## Metodi pubblici di return:
    # estraggo synset data la parola
    def get_synsets_from_word(self, lemma):
        return self.bn_dict[lemma]

    # estraggo lista termini dato il synset
    def get_terms_from_synset(self, bn_sns):
        return self.sns_terms.get(bn_sns)
