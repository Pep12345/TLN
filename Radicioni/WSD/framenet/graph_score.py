import math

from nltk.corpus import framenet as fn
from nltk.corpus import wordnet as wn
from bag_of_words_alg import wsd
from utils import stemmer
from pprint import pprint

def get_big_framenet_context_bow(frame_term):     ### Ctx(w)
    frame = fn.frame(frame_term)
    signature = wsd.extract_words_from_sentence(frame.definition)
    for f in frame.FE:
        signature += wsd.extract_words_from_sentence(frame.FE[f].definition)
    for lu in frame.lexUnit:
        signature += wsd.extract_words_from_sentence(frame.lexUnit[lu].definition)
    return stemmer(signature)


def argmax_prob(wn_word, ctwx, l):
    arg_max = None
    max = -1
    for sns in wn.synsets(wn_word):
        p = probability(sns, wn_word, ctwx, l)
        if p > max:
            max = p
            arg_max = sns
    return arg_max


# probabilità tra synset s e il termine w (passo direttamente il contesto ctwx)
def probability(s, wn_word, ctwx, l):
    nom = score(s, ctwx, l)
    den = 0
    for s1 in wn.synsets(wn_word):
        # for w1 in fn.frames(w):  # non è inutile dal momento che w è un solo frame?
        den += score(s1, ctwx, l)
    return nom/den if nom != 0 else 0


def score(synset, ctxw, l):
    result = 0
    for bow_word in ctxw:
        for sns in wn.synsets(bow_word):
            for path in get_all_paths(sns, synset, l):
                # nel path metto anche il nodo target quindi aggiungo -1 alla formula delle slide
                result += math.exp(-(len(path)-2))
    return result


# restituisce il/i path o [] se non ne trova
def get_all_paths(sns_start, sns_end, length_accepted):
    return bfs_aux([], sns_start, sns_end, length_accepted)


# metodo di appoggio a get_all_paths
# estrae ricorsivamente una lista di path dove ogni path è una list di synset
# nota: nel path aggiunge anche il target quindi serve fare len - 1 dopo
def bfs_aux(history_path, this_node, target, actual_level):

    # se supero la lunghezza accettata termino
    if actual_level == 0:
        return None

    # se trovo il nodo restituisco la concatenazione dei nodi percorsi, il path
    if this_node == target:
        history_path.append(this_node)
        return [history_path]  # [] servono perchè siamo in un contesto "liste di liste"

    # ciclo su ogni iperonimo/iponimo
    queue = [h for h in this_node.hypernyms()]+[h for h in this_node.hyponyms()]
    paths = []

    for sns in queue:
        # questo controllo evita di tornare per nodi già visti
        # senza capitano cose tipo 1-2-3 / 1-4-1-2-3 // cioè ripassa dal nodo di partenza 1
        if sns in history_path:
            continue

        result = bfs_aux(history_path + [this_node], sns, target, actual_level - 1)

        # se result è un nuovo path lo aggiungo alla soluzione
        if result is not None and result:
            paths += result

    return paths


# example get_all_paths
if __name__ == "__main__":
    paths = get_all_paths(wn.synset('dog.n.01'), wn.synset('bitch.n.4'), 10)
    pprint(paths)