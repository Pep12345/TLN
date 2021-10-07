from utils import stemmer
import sys

sys.path.append('..')  # per poter importare file da altri package
from similarity_and_wsd import wsd_ex as wsd


# estraggo la bag of words usando esempi e gloss del synset, dei suoi iperonimi e dei suoi iponimi
def get_wordnet_context_bow(synset):     ### Ctx(s)
    signature = wsd.read_gloss_and_examples(synset)
    for hyp in synset.hypernyms():
        signature += wsd.read_gloss_and_examples(hyp)
    for hyp1 in synset.hyponyms():
        signature += wsd.read_gloss_and_examples(hyp1)
    return stemmer(signature)


#def get_framenet_context_bow(frame_term):     ### Ctx(w)
#frame = fn.frame(frame_term)
#signature = wsd.extract_words_from_sentence(frame.definition)
#for f in frame.FE:
#    signature += wsd.extract_words_from_sentence(frame.FE[f].definition)
#for lu in frame.lexUnit:           # dovrei usare anche la definizione delle lu?
#signature += wsd.extract_words_from_sentence(frame.lexUnit[lu].definition)
#return stemmer(signature)
def get_framenet_context_bow(frame_part):     ### Ctx(w)
    signature = wsd.extract_words_from_sentence(frame_part.definition)
    return stemmer(signature)


### METODI MAPPING SCORE ###

