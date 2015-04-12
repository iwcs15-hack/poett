from wordnet import get_similar
from tweetpos import getPosDict
from poett import generateHaiku, analogyPoem
from random import choice
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
                adjjs, # adjectives
                advbs] # adverbs
    
    return generateHaiku(words, patterns)


default_analogies = [['The ','noun1',' ',2,'s like a ','noun2', '\n',
                      'The ','noun3', ' ',2,'s like a ','noun4'],
                     ['Is it ',3,' that ','noun1','s ',2,' ','noun2','s?\n',
                      'The ','noun3',' ',2,'s ',3,' ','noun4','s.']]

model_path = os.path.join(os.path.dirname(__file__), 'analogyResources', 'GoogleNews-vectors-negative300.bin')
model = Word2Vec.load_word2vec_format(model_path, binary=True)

def analogyFromTweet(tweet, patterns=default_analogies, model=model):
    pos = getPosDict(tweet)
    nouns = grab(pos, ['NN','NNS','NNP','NNPS'])
    verbs = grab(pos, ['VB','VBD','VBP','VBZ','VBN','VBG'])
    adjjs = grab(pos, ['JJ','JJR','JJS'])
    advbs = grab(pos, ['RB','RBR','RBS'])
    
    
    noun1 = choice([x for x in nouns if x in model])
    
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
    
    nouns.remove(noun1)
    
    noun2 = choice([x for x in nouns if x in model])
    
    nouns.remove(noun2)
    
    words = [['o','oh','ooh','ah','lord','god','damn'], # interjections
                nouns, # abstract nouns
                verbs, # intransitive verbs
                adjjs, # adjectives
                advbs] # adverbs
    
    return analogyPoem(noun1, noun2, word_sets=words, patterns=patterns)