from utils import stemmer
import sys

sys.path.append('..')  # per poter importare file da altri package
import importlib
wsd = importlib.import_module("1 similarity_and_wsd.wsd_ex")


# estraggo la bag of words usando esempi e gloss del synset, dei suoi iperonimi e dei suoi iponimi
def get_wordnet_context_bow(synset):     ### Ctx(s)
    signature = wsd.read_gloss_and_examples(synset)
    for hyp in synset.hypernyms():
        signature += wsd.read_gloss_and_examples(hyp)
    for hyp1 in synset.hyponyms():
        signature += wsd.read_gloss_and_examples(hyp1)
    return stemmer(signature)


def get_framenet_context_bow(frame_part):     ### Ctx(w)
    signature = wsd.extract_words_from_sentence(frame_part.definition)
    return stemmer(signature)


