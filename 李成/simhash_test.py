#simhash_test.py
from simhash import Simhash
#去掉标点符号
excludes = {'，','。','/','《','》','？','；','‘','：','“','【','】','{','}',
            '、','|','！','@','#','￥','%','……','&','*','（','）','-','=',
            '——','+','·','~','”',
            ',','.','/','<','>','?',';','\'',':','"','[',']','{','}','\\','|',
            '~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=',
            ' ','\n'}

def getThetxt(str):
    d1 = open(str,encoding='utf-8').read()

    for word in excludes:
        d1 = d1.replace(word,'')
    #print(d1)
    return d1

def simhash_similarity(text1,text2):
    aa_simhash = Simhash(text1)
    bb_simhash = Simhash(text2)
    max_hashbit = max(len(bin(aa_simhash.value)),len(bin(bb_simhash.value)))
    #汉明距离
    distince = aa_simhash.distance(bb_simhash)
    similar = 1 - distince/max_hashbit
    return similar

if __name__ == '__main__':

    first = getThetxt('C:/Users/60917/Desktop/第一章.txt')
    second = getThetxt('C:/Users/60917/Desktop/第二章.txt')
    third = getThetxt('C:/Users/60917/Desktop/第三章.txt')

    print(simhash_similarity(first, third))
    print(simhash_similarity(second, third))
