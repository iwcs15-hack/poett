# -*- coding: utf-8 -*-

import nltk
import json


with open('london-marathon-2015-03-18') as f:
    for line in f:
        tweet = json.loads(line)
        
        # Tokenize Text
        tokens = tweet['text'].split(' ')
        
        # Get POS Tags
        posTags = nltk.pos_tag(tokens)
        
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
                
        
        