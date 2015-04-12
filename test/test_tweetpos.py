# -*- coding: utf-8 -*-

from src.tweetpos import getTweetPOS
                
if __name__ == "__main__":
    
    posDicts = []
    
    with open('test/london-marathon-2015-03-18') as f:
        for line in f:
            posDicts.append(getTweetPOS(line))
    
    print(posDicts)