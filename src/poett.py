from random import choice
from random import randint

cnouns=['shark','whale','tuna']
anouns=['adventure','courage','endurance']
tverbs=['command','view','lead']
iverbs=['travel','sail','wave']
adjs=['big','small','old']

def generatePoem(cnouns,anouns,tverbs,iverbs,adjs):
    adverbs=['quickly','loudly','calmly','quietly','roughly']
    interjections=['o','oh','ooh','ah','lord','god','damn']


    p1=['The ',5,' ',1,' ',6,' ',3,'s ','the ',1,'.']
    p2=[5,', ',5,' ',1,'s ',6,' ',3, ' a ',5,', ',5,' ',1]
    p3=['Why does the ',1, ' ',4,'?']
    p4=[4,' ',6,' like a ',5,' ',1,'.']
    p5=[2,', ',2,' and ',2,'.']
    p6=['Where is the ',5,' ',1,'?']
    p7=['All ',1,'s ',3,' ',5,', ',5,' ',1,'s.']
    p8=['Never ',3,' a ',1,'.']
    p9=[2,' is a ',5, ' ',1,'.']
    p10=[9,', ',2, '!']
    p11=[1,'s ',4,'!']
    p12=['The ',1,' ',4,'s like a ',5,' ',1,'. ']
    p13=[1,'s ',4,' like ',5,' ',1,'s.']

    patterns=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13]

    l = randint(1,4)
    poem = ''
    for i in range(l):
        pattern = choice(patterns)
        output = ''
        for x in pattern:
            if x==1:
                output += choice(cnouns)
            elif x==2:
                output += choice(anouns)
            elif x==3:
                output += choice(tverbs)
            elif x==4:
                output += choice(iverbs)
            elif x==5:
                output += choice(adjs)
            elif x==6:
                output += choice(adverbs)
            elif x==9:
                output += choice(interjections)
            else:
                output += x
        poem += output
        if i < (l-1):
            poem += '\n'
    return poem

print(generatePoem(cnouns,anouns,tverbs,iverbs,adjs))
