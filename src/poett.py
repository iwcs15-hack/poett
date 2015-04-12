from random import choice, randint
#from phonetics import syllables
from phonetics import rhymes
from analogyResources.gensim.models.word2vec import Word2Vec
import os.path

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

def analogyPoem(noun1, noun2, model, word_sets):
    """
    Picks randomly between patterns
    Puts noun1 in the first noun slot, noun2 in the second noun slot
    Finds a noun that rhymes with noun2 for the 4th noun slot
    Finds a noun that matches the analogy for the 3rd noun slot
    """
    patterns=[['The ',noun1,' ',3,'s like a ',noun2, '\n',
                'The ','noun3', ' ',3,'s like a ','noun4'],
              ['Is it ',5,' that ',noun1,'s ',3,' ',noun2,'s?\n',
                'The ','noun3',' ',3,'s ',5,' ','noun4','s.']
            ]
    poem= ''
    noun4=''
    pattern = choice(patterns)
    for n, x in enumerate(pattern):
        if x == 'noun4':
            while noun4=='':
                noun = choice(list(rhymes(noun2)))
                if noun in model:
                    noun4= noun
                    pattern[n] = noun4
    for x in pattern:
        word = None
        if x == 'noun3':
            poem += model.most_similar(positive=[noun1,noun4],negative=[noun2])[0][0]
        elif type(x) == int:
            poem += choice(word_sets[x])
        else:
            poem += x
    return poem



if __name__ == '__main__':
    words = [['o','oh','ooh','ah','lord','god','damn'], # interjections 0
             ['shark','whale','tuna'], # concrete nouns 1
             ['adventure','courage','endurance'], # abstract nouns 2
             ['command','view','lead'], # transitive verbs 3
             ['travel','sail','wave'], # intransitive verbs 4
             ['big','small','old'], # adjectives 5
             ['quickly','loudly','calmly','quietly','roughly']] # adverbs 6

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

    model_path = os.path.join(os.path.dirname(__file__), 'analogyResources', 'GoogleNews-vectors-negative300.bin')
    model = Word2Vec.load_word2vec_format(model_path, binary=True)
    print(analogyPoem('darkness','night',model,words))
    print(analogyPoem('sea', 'mermaid', model,words))
    print(analogyPoem('death','lover', model, words))
    print(generatePoem(words, patterns))
