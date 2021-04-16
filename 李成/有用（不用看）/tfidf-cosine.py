#名字就是算法，可用

import math

from userful.tfidfOfM import getTheTFIDF

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

    return d1

def compute_cosine(dic_f, dic_s):

    # print("dic_f:{}".format(dic_f))
    # print("dic_s:{}".format(dic_s))

    first_dict = {}
    for word in dic_f:
            first_dict[word[0]] = word[1]

    second_dict = {}
    for word in dic_s:
            second_dict[word[0]] = word[1]
    #得到词向量（两者的所有的）
    keyWords = []

    for i in range(len(dic_f)):
        keyWords.append(dic_f[i][0])    #添加数组（都是字）

    for i in range(len(dic_s)):
        if dic_s[i][0] in keyWords: #有的话啥也不干
            pass
        else:                       #没有就加入
            keyWords.append(dic_s[i][0])
    vect_f = []
    vect_s = []

    for word in keyWords:
        if word in first_dict:
            vect_f.append(first_dict[word])
        else:
            vect_f.append(0)
        if word in second_dict:
            vect_s.append(second_dict[word])
        else:
            vect_s.append(0)
    print("vect_f:{}".format(vect_f))
    print("vect_s:{}".format(vect_s))

    #开始计算余弦相似度
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(vect_f)):
        sum += vect_f[i] * vect_s[i]
        sq1 += pow(vect_f[i],2)
        sq2 += pow(vect_s[i],2)
    try:    #round() 四舍五入,结果保留两位小数
        result = round(float(sum)/(math.sqrt(sq1)*math.sqrt(sq2)),2)
    except ZeroDivisionError:
        result = 0.0
    return result

if __name__ == '__main__':

    first = 'C:/Users/60917/Desktop/a.txt'
    second = 'C:/Users/60917/Desktop/b.txt'
    third = 'C:/Users/60917/Desktop/c.txt'
    forth = 'C:/Users/60917/Desktop/d.txt'
    # 获得字符串,去掉标点，尚未分词
    f = getThetxt(first)
    s = getThetxt(second)
    t = getThetxt(third)
    fo = getThetxt(forth)
    database = [f,s,t,fo ]
    Tfidf_list = []
    for i in range(len(database)):
        Tfidf_list.append(getTheTFIDF(i,database))

    print(compute_cosine(Tfidf_list[0],Tfidf_list[1]))
    print(compute_cosine(Tfidf_list[1],Tfidf_list[2]))

