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

def haikuFromTweet(tweet):
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
    
    words_ly = [['o','oh','ooh','ah','lord','god','damn'], # interjections
                nouns, # concrete nouns
                nouns, # abstract nouns
                verbs, # transitive verbs
                verbs, # intransitive verbs
                adjjs, # adjectives
                adjjs] # adverbs minus -ly
        
    syll_pats =[[['The ',5,' ',1,' ',6,'ly ',3,'s ','the ',1,'.'], 3],
                [[5,', ',5,' ',1,'s ',6,'ly ',3, ' a ',5,', ',5,' ',2], 1],
                [['Why does the ',1, ' ',4,'?'], 3],
                [[4,' ',6,'ly like a ',5,' ',1,'.'], 3],
                [[2,', ',2,' and ',2,'.'], 1],
                [['Where is the ',5,' ',1,'?'], 3],
                [['All ',1,'s ',3,' ',5,', ',5,' ',1,'s.'], 1],
                [['Never ',3,' a ',1,'.'], 3],
                [[2,' is a ',5, ' ',1,'.'], 2],
                [[0,', ',2, '!'], 0],
                [[1,'s ',4,'!'], 0],
                [['The ',1,' ',4,'s like a ',5,' ',1,'. '], 3],
                [[1,'s ',4,' like ',5,' ',1,'s.'], 1]]
    
    return generateHaiku(words_ly, syll_pats)