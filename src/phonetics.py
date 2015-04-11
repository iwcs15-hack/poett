from nltk import cmudict
cmu = cmudict.dict()
from collections import defaultdict

RHYME_SETS = defaultdict(set)

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

def ending(phonemes):
    """
    Returns the ending of a string of syllables,
    from the last stressed syllable
    """
    n = len(phonemes) - 1
    found = False
    # Find the last stressed vowel
    while not found and n >= 0:
        if phonemes[n][-1] in ('1','2'):
            found = True
        else:
            n -= 1
    # In case there are no stressed vowels
    if not found and n >= 0:
        n = len(phonemes) - 1
        while not found:
            if phonemes[n][-1] in ('0','1','2'):
                found = True
            else:
                n -= 1
    # If there are no vowels, this will return the whole string
    return tuple(phonemes[n:])

# Find words with the same ending
for word, phon in cmu.items():
    for p in phon:
        RHYME_SETS[ending(p)].add(word)

def rhymes(word):
    """
    Given an input word,
    return a set of rhyming words
    """
    output = set()
    for pron in cmu[word]:
        output |= RHYME_SETS[ending(pron)]
    return output