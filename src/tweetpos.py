# -*- coding: utf-8 -*-

import nltk
import json
import re
from html.parser import HTMLParser
import random

wn = nltk.corpus.wordnet


        
def tokenizeTweet(text):
    
        """ Tokenize Text
        """
        text = text.replace('\n', ' ')
        text = text.replace('?', ' ?')
        text = text.replace('!', ' !')
        text = text.replace('...', ' ')
        text = re.sub("[^;:\-,'^]\(", ' ( ', text)
        text = re.sub('([A-Za-z0-9])\)', '\g<1> ) ', text)
        text = re.sub('http[s]?:[^ ]+', '', text)
        text = re.sub('\u003e','',text)
        tokens = text.split(' ')
        
        # Remove empty tokens
        tokens = list(filter(None, tokens))

        '''
        tokenization = nltk.word_tokenize(tweet['text']) 
        #tweet['text'].split(" ")
        
        at = False
        hashTag = False
        
        tweetTokenization = []
        
        for token in tokenization:
            if at == True: 
                at = False
                tweetTokenization.append('@'+token)
            elif hashTag == True: 
                hashTag = False
                tweetTokenization.append('#'+token)
            elif token =='@':
                at = True
            elif token == '#':
                hashTag = True
            else:
                tweetTokenization.append(token)
                '''
        return(tokens)


def getTweetPOS(line, lemmatize=False):
    """
    Given a list of tokens,
    return a dictionary from tags to sets of tokens
    """
  
    # Get POS Tags
    posTags = nltk.pos_tag(line)
    
    # Lemmatize if required
    if lemmatize:
        for n, x in enumerate(posTags):
            token, tag = x
            lemma = None
            if tag in ['VB','VBD','VBN','VBG','VBZ','VBP']:
                lemma = wn.morphy(token,wn.VERB)
            elif tag in ['NN', 'NNS', 'NNP', 'NNPS']:
                lemma = wn.morphy(token,wn.NOUN)
            elif tag in ['JJ', 'JJR', 'JJS']:
                lemma = wn.morphy(token,wn.ADJ)
            elif tag in ['RB', 'RBR', 'RBS']:
                lemma = wn.morphy(token,wn.ADV)
            if lemma:
                posTags[n] = (lemma, tag)
    
    posDict = dict()
    
    for posTag in posTags:
        if posTag[0].startswith("@"):
            if not 'NNP' in posDict:
                posDict['NNP'] = set()
            posDict['NNP'].add(posTag[0])      
        else:
            if not posTag[1] in posDict:
                posDict[posTag[1]] = set()
            posDict[posTag[1]].add(posTag[0])
    
    return posDict


def getPosDict(text):
    """
    From raw text, return a dict from POS tags to sets of lemmas
    """
    return getTweetPOS(tokenizeTweet(text), True)


def getTweetText(line):
    tweet = json.loads(line)
    if tweet['text'].startswith("RT") and 'retweeted_status' in tweet:
        text = tweet['retweeted_status']['text']
    else:
        text = tweet['text']
    
    text = HTMLParser().unescape(text)
    text = text.encode('ascii','ignore').decode('utf8','ignore') #decode('unicode_escape').encode('ascii','ignore')
    return text
    
if __name__ == "__main__":
    with open('2015-03-22') as f:
        for line in f:
            text = getTweetText(line)
            
            #text = "First @LDN_Muscle lifting session since christmas due to London Marathon training, god I've missed it! Completely different kind of Work"
            
            tokens = tokenizeTweet(text)
            # Get POS Tags
            posTags = getTweetPOS(tokens)
            
            print(posTags)
            
            if 'CD' in posTags:
                cd = random.sample(posTags['CD'], 1)[0]
            else:
                cd = 2
            
            if 'NN' in posTags:
                nn = random.sample(posTags['NN'],1)[0]
            else:
                nn = 'road'
            
            if 'NNP' in posTags:
                nnp = random.sample(posTags['NNP'],1)[0]
            else:
                nnp = 'I'
                
            if 'RB' in posTags:
                rb = random.sample(posTags['RB'],1)[0]
            else:
                rb = 'less'
            
            if 'VBG' in posTags:
                vbg = random.sample(posTags['VBG'],1)[0]
            else:
                vbg = 'difference'
            
            
            #print(posTags)
            print(str(cd) + ' ' + nn + 's diverged in a wood, and ' + nnp + '--\n' + nnp + ' took the one ' + rb + ' traveled by,\n' + 'And that has made all the ' + vbg + '\n')
