from random import choice, randint
from phonetics import syllables, rhymes
from collections import defaultdict
from analogyResources.gensim.models.word2vec import Word2Vec
import os.path

def generatePoem(word_sets, pattern_list, N=None):
    """
    From sets of words and patterns, generate a poem
    """
    poem = ''
    if N == None:
        N = randint(1,4)
    for i in range(N):
        pattern = choice(pattern_list)
        line = ''
        for x in pattern:
            if type(x) == int:
                line += choice(word_sets[x])
            else:
                line += x
        poem += line.capitalize()
        if i < (N-1):
            poem += '\n'
    return poem

def generateHaikuLine(word_syll_sets, filtered_list):
    """
    From sets of words with syllables,
    and patterns with syllable sequences,
    generate a haiku.
    """
    pattern, seq_set = choice(filtered_list)
    sequence = choice(seq_set)
    line = ''
    current = 0
    for x in pattern:
        if type(x) == int:
            sylls = sequence[current]
            line += choice(word_syll_sets[x][sylls])
            current += 1
        else:
            line += x
    return line.capitalize()

def generateHaiku(word_sets, pattern_list):
    """
    From sets of words and patterns (with syllable counts),
    generate a haiku.
    Raises an error if no haiku is possible.
    """
    word_sylls = []
    pattern_sylls = []
    # Calculate what numbers of syllables are possible for each word set
    for s in word_sets:
        word_sylls.append(defaultdict(set))
        for w in s:
            for n in syllables(w):
                word_sylls[-1][n].add(w)
    word_sylls = [{x:list(y) for x,y in l.items()} for l in word_sylls] # Change defaultdict of sets to dict of lists
    # Calculate what numbers of syllables are possible for each pattern
    for p, n in pattern_list:
        previous = {n:{tuple()}}
        current = defaultdict(set)
        for x in p:
            if type(x) != int:
                continue
            for i, seq_set in previous.items():
                for j in word_sylls[x]:
                    paths = {s + (j,) for s in seq_set}
                    current[i+j] |= paths
            previous = current
            current = defaultdict(set)
        pattern_sylls.append(dict(previous))
    # Filter out patterns which allow 5 or 7 syllables
    five = []
    seven = []
    for i, p in enumerate(pattern_list):
        p = p[0]
        if 5 in pattern_sylls[i]:
            five.append([p, list(pattern_sylls[i][5])])
        if 7 in pattern_sylls[i]:
            seven.append([p, list(pattern_sylls[i][7])])
    
    lines = []
    lines.append(generateHaikuLine(word_sylls, five))
    lines.append(generateHaikuLine(word_sylls, seven))
    lines.append(generateHaikuLine(word_sylls, five))
    
    return('\n'.join(lines))
    

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
    """
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
    
    words_ly = [['o','oh','ooh','ah','lord','god','damn'], # interjections
                ['shark','whale','tuna'], # concrete nouns
                ['adventure','courage','endurance'], # abstract nouns
                ['command','view','lead'], # transitive verbs
                ['travel','sail','wave'], # intransitive verbs
                ['big','small','old'], # adjectives
                ['quick','loud','calm','quiet','rough']] # adverbs minus -ly
    
    syll_pats =[[['The ',5,' ',1,' ',6,'ly ',3,'s ','the ',1,'.'], 3],
                [[5,', ',5,' ',1,'s ',6,'ly ',3, ' a ',5,', ',5,' ',2], 1],
                [['Why does the ',1, ' ',4,'?'], 3],
                [[4,' ',6,'ly like a ',5,' ',1,'.'], 3],
                [[2,', ',2,' and ',2,'.'], 1],
                [['Where is the ',5,' ',1,'?'], 3],
                [['All ',1,'s ',3,' ',5,', ',5,' ',1,'s.'], 1],
                [['Never ',3,' a ',1,'.'], 2],
                [[2,' is a ',5, ' ',1,'.'], 2],
                [[0,', ',2, '!'], 0],
                [[1,'s ',4,'!'], 0],
                [['The ',1,' ',4,'s like a ',5,' ',1,'. '], 3],
                [[1,'s ',4,' like ',5,' ',1,'s.'], 1]]
    
    print(generateHaiku(words_ly, syll_pats))
    """

    model_path = os.path.join(os.path.dirname(__file__), 'analogyResources', 'GoogleNews-vectors-negative300.bin')
    model = Word2Vec.load_word2vec_format(model_path, binary=True)
    print(analogyPoem('darkness','night',model,words))
    print(analogyPoem('sea', 'mermaid', model,words))
    print(analogyPoem('death','lover', model, words))
    print(generatePoem(words, patterns))