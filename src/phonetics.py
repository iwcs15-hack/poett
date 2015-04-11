from nltk import cmudict
cmu = cmudict.dict()

def phon_to_syllables(phonemes):
    """
    Returns the number of syllables in a string of phonemes
    """
    n = 0
    for p in phonemes:
        if p[-1] in ('0','1','2'):
            n += 1
    return n

def syllables(word):
    """
    Returns possible numbers of syllables in a word
    """
    return set(phon_to_syllables(x) for x in cmu[word])