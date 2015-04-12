from nltk.corpus import wordnet as wn

# immediate hyponyms of the root synset 'entity':
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

def get_hyponyms(lemma):
    """
    Given an input string,
    return all lemmas in the full hyponym
    """
    hypo = set()
    search = set(wn.synsets(lemma))
    while search:
        current = search.pop()
        search |= set(current.hyponyms())
        for lem in current.lemmas():
            hypo.add(lem.name())
    return(hypo)

def get_immediate_hyponyms(synsets):
    """
    Given a set of synsets,
    return immediate hyponyms of those synsets
    """
    hypo = set()
    for s in synsets:
        hypo |= set(s.hyponyms())
    return hypo

def get_hyponyms_upto(lemma, n=3):
    """
    Given a string,
    return all hyponyms up to a given depth n
    """
    current = wn.synsets(lemma)
    all = {lem.name() for s in current for lem in s.lemmas()}
    for i in range(n):
        current = get_immediate_hyponyms(current)
        all |= {lem.name() for s in current for lem in s.lemmas()}
    return all

def get_similar(lemma, pos=None):
    """
    Given an input string,
    return similar lemmas
    """
    similar = set()
    if pos:
        syns = wn.synsets(lemma, pos)
    else:
        syns = wn.synsets(lemma)
    for sense in syns:
        for hyper in sense.hypernyms():
            for hypo in hyper.hyponyms():
                for new_lem in hypo.lemmas():
                    similar.add(new_lem.name())
    return similar