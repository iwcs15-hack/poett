from nltk.corpus import cmudict
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
    output.remove(word)
    return output

def find_rhymes(words):
    """
    Given a set of words,
    find subsets of words that rhyme
    """
    endings = defaultdict(set)
    for w in words:
        try:
            for pron in cmu[w]:
                endings[ending(pron)].add(w)
        except KeyError:
            print(w, 'not found in CMU dictionary')
    return [x for x in endings.values() if len(x) > 1]