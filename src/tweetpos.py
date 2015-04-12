# -*- coding: utf-8 -*-

import nltk
import json
import re



        
def tokenizeTweet(text):
    
        """ Tokenize Text
        """
        text = text.replace('\n', ' ')
        text = text.replace('?', ' ?')
        text = text.replace('!', ' !')
        text = text.replace('...', ' ')
        text = re.sub("[^;:\-,'^]\(", ' ( ', text)
        text = re.sub('([A-Za-z0-9])\)', '\g<1> ) ', text)
        text = re.sub('https?:[^ ]+', '', text)
        tokens = text.split(' ')

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


def getTweetPOS(line):
    """
    Given a list of tokens,
    return a dictionary from tags to sets of tokens
    """
  
    # Get POS Tags
    posTags = nltk.pos_tag(line)
    
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

def getTweetText(line):
    tweet = json.loads(line)
    if tweet['text'].startswith("RT"):
        return tweet['retweeted_status']['text']
    else:
        return tweet['text']
    
if __name__ == "__main__":
    with open('london-marathon-2015-03-18') as f:
        for line in f:
            
            text = getTweetText(line)
            tokens = tokenizeTweet(text)
            # Get POS Tags
            posTags = getTweetPOS(tokens)
            print(posTags)



