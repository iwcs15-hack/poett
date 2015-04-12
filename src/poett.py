from random import choice, randint
#from phonetics import syllables

def generatePoem(word_sets, pattern_list):
    """
    From sets of words and patterns, generate a poem 
    """
    poem = ''
    l = randint(1,4)
    for i in range(l):
        pattern = choice(pattern_list)
        line = ''
        for x in pattern:
            if type(x) == int:
                line += choice(word_sets[x])
            else:
                line += x
        poem += line.title()
        if i < (l-1):
            poem += '\n'
    return poem


if __name__ == '__main__':
    words = [['o','oh','ooh','ah','lord','god','damn'], # interjections
             ['shark','whale','tuna'], # concrete nouns
             ['adventure','courage','endurance'], # abstract nouns
             ['command','view','lead'], # transitive verbs
             ['travel','sail','wave'], # intransitive verbs
             ['big','small','old'], # adjectives
             ['quickly','loudly','calmly','quietly','roughly']] # adverbs
    
    patterns = [['The ',5,' ',1,' ',6,' ',3,'s ','the ',1,'.'],
                [5,', ',5,' ',1,'s ',6,' ',3, ' a ',5,', ',5,' ',1],
                ['Why does the ',1, ' ',4,'?'],
                [4,' ',6,' like a ',5,' ',1,'.'],
                [2,', ',2,' and ',2,'.'],
                ['Where is the ',5,' ',1,'?'],
                ['All ',1,'s ',3,' ',5,', ',5,' ',1,'s.'],
                ['Never ',3,' a ',1,'.'],
                [2,' is a ',5, ' ',1,'.'],
                [0,', ',2, '!'],
                [1,'s ',4,'!'],
                ['The ',1,' ',4,'s like a ',5,' ',1,'. '],
                [1,'s ',4,' like ',5,' ',1,'s.']]
    
    print(generatePoem(words, patterns))
