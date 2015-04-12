# -*- coding: utf-8 -*-

import nltk
import json
import re



        
def tokenizeTweet(text)
        """ Tokenize Text
        """
        text = tweet['text'].replace('\n', ' ')
        text = text.replace('?', ' ?')
        text = text.replace('!', ' !')
        text = text.replace('...', ' ')
        text = re.sub("[^;:\-,'^]\(", ' ( ', text)
        text = re.sub('([A-Za-z0-9])\)', '\g<1> ) ', text)
        text = re.sub('http://[^ ]+', '', text)
        tokens = text.split(' ')

        return(tokens)


def getTweetPOS(line):
    tweet = json.loads(line)
    tokens = tokenizeTweet(tweet)
    
    # Get POS Tags
    posTags = nltk.pos_tag(tokens)
    
    posDict = dict()
    
    for posTag in posTags:
        if posTag[0].startswith("@"):
            if not 'NNP' in posDict:
                posDict['NNP'] = list()
            posDict['NNP'].append(posTag[0])      
        else:
            if not posTag[1] in posDict:
                posDict[posTag[1]] =list()
            posDict[posTag[1]].append(posTag[0])
    
    return posDict

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
