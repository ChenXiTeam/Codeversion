import math
import re
import datetime
import time
import jieba
import gensim
#单纯的余弦相似度算法，目前来说应该用tfidf-的余弦相似度算法
#剔除标点符号
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
def getTheFrequency(list):
    dict = {}
    for word in list:
        if word != '' and word in dict:
            num = dict[word]
            dict[word] = num + 1
        elif word != '':
            dict[word] = 1
        else:
            continue
    return dict

def compute_cosine(txt_a, txt_b):
    first = getThetxt(txt_a)
    second = getThetxt(txt_b)

    first_list = [word for word in jieba.cut(first)]
    second_list = [word for word in jieba.cut(second)]

    #频率获得  从list 到 dict
    first_dict = getTheFrequency(first_list)
    second_dict = getTheFrequency(second_list)


    #排序
    dic_f = sorted(first_dict.items(),key=lambda asd:asd[1],reverse=True)
    dic_s = sorted(second_dict.items(),key=lambda asd:asd[1],reverse=True)
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
    #开始计算余弦相似度
    sum = 0
    sq1 = 0
    sq2 = 0
    for i in range(len(vect_f)):
        sum += vect_f[i] * vect_s[i]
        sq1 += pow(vect_f[i],2)
        sq2 += pow(vect_s[i], 2)
    try:    #round() 四舍五入,结果保留两位小数
        result = round(float(sum)/(math.sqrt(sq1)*math.sqrt(sq2)),2)
    except ZeroDivisionError:
        result = 0.0
    return result

if __name__ == '__main__':

    print(compute_cosine('C:/Users/60917/Desktop/第一章.txt','C:/Users/60917/Desktop/第三章.txt'))
    print(compute_cosine('C:/Users/60917/Desktop/第二章.txt','C:/Users/60917/Desktop/第三章.txt'))

