from wordnet import get_similar
from tweetpos import getPosDict
from poett import generateHaiku
from nltk.corpus import wordnet as wn, cmudict
cmu = cmudict.dict()

def grab(word_dict, tags):
    output = set()
    for t in tags:
        if t in word_dict:
            output |= word_dict[t]
    return output

default_patterns=[[['The ',3,' ',1,' ',3,'ly ',2,'s ','the ',1,'.'], 3],
                  [[3,', ',3,' ',1,'s ',3,'ly ',3, ' a ',3,', ',3,' ',1], 1],
                  [['Why does the ',1, ' ',2,'?'], 3],
                  [[2,' ',3,'ly like a ',3,' ',1,'.'], 3],
                  [[1,', ',1,' and ',1,'.'], 1],
                  [['Where is the ',3,' ',1,'?'], 3],
                  [['All ',1,'s ',2,' ',3,', ',3,' ',1,'s.'], 1],
                  [['Never ',2,' a ',1,'.'], 3],
                  [[1,' is a ',3, ' ',1,'.'], 2],
                  [[0,', ',1, '!'], 0],
                  [[1,'s ',2,'!'], 0],
                  [['The ',1,' ',2,'s like a ',3,' ',1,'. '], 3],
                  [[1,'s ',2,' like ',3,' ',1,'s.'], 1]]

def haikuFromTweet(tweet, patterns=default_patterns):
    pos = getPosDict(tweet)
    nouns = grab(pos, ['NN','NNS','NNP','NNPS'])
    verbs = grab(pos, ['VB','VBD','VBP','VBZ','VBN','VBG'])
    adjjs = grab(pos, ['JJ','JJR','JJS'])
    advbs = grab(pos, ['RB','RBR','RBS'])
    
    for n in nouns.copy():
        nouns |= get_similar(n, wn.NOUN)
    for v in verbs.copy():
        verbs |= get_similar(v, wn.VERB)
    for j in adjjs.copy():
        adjjs |= get_similar(j, wn.ADJ)
    for b in advbs.copy():
        advbs |= get_similar(b, wn.ADV)
    
    for wordset in [nouns, verbs, adjjs, advbs]:
        for x in wordset.copy():
            if not x in cmu:
                wordset.remove(x)
    
    words = [['o','oh','ooh','ah','lord','god','damn'], # interjections
                nouns, # abstract nouns
                verbs, # intransitive verbs
                adjjs,
                advbs] # adverbs minus -ly
    
    return generateHaiku(words, patterns)