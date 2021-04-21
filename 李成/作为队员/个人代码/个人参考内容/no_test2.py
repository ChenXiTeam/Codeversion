
import re
import string
excludes = {'，','。','/','《','》','？','；','‘','：','“','【','】','{','}',
            '、','|','！','@','#','￥','%','……','&','*','（','）','-','=',
            '——','+','·','~','”',
            ',','.','/','<','>','?',';','\'',':','"','[',']','{','}','\\','|',
            '~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','='}
excludes2 = {"\n",'\'','\"','\xe5','\xe7','\t','\0'}


def getThetxt(str):
    d1 = open(str,encoding='utf-8').read()

    for word in excludes2:
        d1 = d1.replace(word," ")

    print(d1.replace('\\',''))
    return d1


first = 'C:/Users/60917/Desktop/新建文本文档.txt'
f = getThetxt(first)
