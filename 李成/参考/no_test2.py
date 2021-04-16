
import re
import string
excludes = {'，','。','/','《','》','？','；','‘','：','“','【','】','{','}',
            '、','|','！','@','#','￥','%','……','&','*','（','）','-','=',
            '——','+','·','~','”',
            ',','.','/','<','>','?',';','\'',':','"','[',']','{','}','\\','|',
            '~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','='}

def getThetxt(str):
    d1 = open(str,encoding='utf-8').read()

    for word in excludes:
        d1 = d1.replace(word," ")

    print(d1)
    return d1


first = 'C:/Users/60917/Desktop/第一章.txt'
f = getThetxt(first)
