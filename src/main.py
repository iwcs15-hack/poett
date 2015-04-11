from nltk.corpus import wordnet as wn

TOP = {wn.synset('abstraction.n.06'):'ABS',
       wn.synset('physical_entity.n.01'):'CONC',
       wn.synset('thing.n.08'):'CONC'}

def conc_or_abs(lemma):
    """
    Given an input string, will return one of:
     'ABS'  - abstract noun
     'CONC' - concrete noun
     'BOTH' - either abstract or concrete
     None   - not found
    """
    intermediate = set(wn.synsets(lemma))
    if not intermediate:
        return None
    top_level = set()
    while intermediate:
        current = intermediate.pop()
        if current in TOP:
            top_level.add(TOP[current])
        else:
            intermediate |= set(current.hypernyms())
    if len(top_level) == 2:
        top_level = {'BOTH'}
    return top_level.pop()