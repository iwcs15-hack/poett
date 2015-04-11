# -*- coding: utf-8 -*-

import nltk
import json
from nltk.tag.brill import Pos


with open('london-marathon-2015-03-18') as f:
    for line in f:
        tweet = json.loads(line)
        
        # Tokenize Text
        text = tweet['text'].replace('\n', ' ')
        text = text.replace('?', ' ?')
        text = text.replace('...', ' ')
        tokens = text.split(' ')
        
        # Get POS Tags
        posTags = nltk.pos_tag(tokens)
        
        print(posTags)
        
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
                
        
        