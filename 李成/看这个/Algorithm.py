#这个.py将所有的算法集成起来
import math
import jieba
import numpy as np
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity
from simhash import Simhash
from collections import Counter

#0.一些都要用到的方法
#数据处理，将字符串分词,data是一个字符串，返回值是一个Counter类型
def dataprocess(data):
    sentence_list = [word for word in jieba.cut(data)]
    count = Counter(sentence_list)
    return count

#1.simhash算法     simhash_similarity_list(sqllist)
#输入：text1以及text2是两个字符串
#输出：相似度计算结果
def simhash_similarity(text1,text2):
    aa_simhash = Simhash(text1)
    bb_simhash = Simhash(text2)
    max_hashbit = max(len(bin(aa_simhash.value)),len(bin(bb_simhash.value)))
    #汉明距离
    distince = aa_simhash.distance(bb_simhash)
    similar = 1 - distince/max_hashbit
    return round(similar,2)

#输入一个字符串list 例如:['1123','32123','123123213'],没有分词,没去标点
#输出{0: (2, 0.65), 1: (0, 0.61), 2: (0, 0.65), 3: (0, 0.49)}
#意思是0和2最相似,相似度为0.65,后面类似
def get_simhash_similarity(database):
    #使用第一个算法.
    #可优化
    resdict_simhash = {}

    for i,s in enumerate(database):
        list_i = []
        # if j == len(sqllist):
        #     break;
        for j in range(len(database)):
            list_i.append(simhash_similarity(s,database[j]))

        # print(list_i)
        resdict_simhash[i] = list_i
        # print(reslist_simhash)

    dict_result = {}

    for i in range(len(resdict_simhash)):
        max = 0
        resdict_simhash[i][i] = 0
        for j in range(len(resdict_simhash.get(i))):

            if resdict_simhash[i][j] > max :
                max = resdict_simhash[i][j]
                dict_result[i] = (j,max)

    return dict_result

#2.TFIDF
# tfidf 算法
def tf(word,count):
    return count[word]/sum(count.values())
def n_containing(word,count_list):
    return sum(1 for count in count_list if word in count)
def idf(word,count_list):
    return math.log10(len(count_list)/(1+n_containing(word,count_list)))
def tfidf(word,count,count_list):
    return tf(word,count)*idf(word,count_list)
#计算数据库中第location+1的TFIDF
# location 是int database 是list [获得字符串,去掉标点，尚未分词]
#database是指字符串list，有很多个
def getTheTFIDF(location,database):

    if location>=len(database):
        print("location is wrong!")
        return ;

    wordlist = []
    for data in database :
        wordlist.append(dataprocess(data))

    # print("2@@@@@@")
    # print(wordlist)
    # print("2@@@@@@")

    for i,count in enumerate(wordlist):

        if i==location:
            # print("Top words in document{}:".format(i + 1))
            # 计算每个词的tfidf
            #   出现负值，原因 idf是 负的，所有文档中都有，所以应该挑选所有大于0的

            # scores = {word: tfidf(word, count, wordlist) for word in count}
            scores = {}
            for word in count:
                width = tfidf(word, count, wordlist)
                if width > 0:
                    scores[word] = width
                else:
                    scores[word] = 0

            sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            #格式化输出
            # for word, score in sorted_words[:10]:
            #     print('\tWord:{},TF-IDF:{}'.format(word, round(score, 5)))
            return sorted_words;

#3.基于tfidf的余弦相似度算法
#list_f与list_s,是两个list，但是其中的内容是元组，如下
#[('李成', 0.10034333188799373), ('我', 0), ('是', 0)]
#结合上面的TFIDF使用，方法如下
# Tfidf_list = []
# for i in range(len(database)):
#       Tfidf_list.append(getTheTFIDF(i,database))
#print(compute_cosine(Tfidf_list[0],Tfidf_list[1]))

def compute_cosine(list_f, list_s):

    # print("dic_f:{}".format(dic_f))
    # print("dic_s:{}".format(dic_s))

    first_dict = {}
    for word in list_f:
            first_dict[word[0]] = word[1]

    second_dict = {}
    for word in list_s:
            second_dict[word[0]] = word[1]
    #得到词向量（两者的所有的）
    keyWords = []

    for i in range(len(list_f)):
        keyWords.append(list_f[i][0])    #添加数组（都是字）

    for i in range(len(list_s)):
        if list_s[i][0] in keyWords: #有的话啥也不干
            pass
        else:                       #没有就加入
            keyWords.append(list_s[i][0])
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
        # result = round(float(sum)/(math.sqrt(sq1)*math.sqrt(sq2)),2)
        result = float(sum) / (math.sqrt(sq1) * math.sqrt(sq2))
    except ZeroDivisionError:
        result = 0.0
    return result

#4.最大字符子串  主要是LongSubstringSim(database,x)
#主要调用getSimilar(A,B,x)
#输入：A，B是字符串，x是阈值代表计入大于x的子串
#输出：计算获得的相似度
def getSimilar(A,B,x):

    a = int(getSubstring2(A, B,x))
    similar = round( (2.0 * a ) / (len(A)+len(B)),2)
    return similar

#字符长度大于x计入
def getSubstring2(a,b,x):

    list_a = list(a)
    list_b = list(b)
    max_s = (max(len(a),len(b)))
    list2 = np.zeros((max_s,max_s))

    for i in range(len(list_a)):
        for j in range(len(list_b)):
            if list_a[i]==list_b[j] :
                if i<1 or j < 1:
                    list2[i][j] = 1
                else:
                    list2[i][j] = list2[i-1][j-1]+1

    # print(list2)

    sum_number = 0
    max_number = 0
    for i in range(max_s):
        for j in range(max_s):
            ii = i
            jj = j
            #斜方向向下找
            while ii+1 < max_s and jj+1 < max_s and list2[ii+1][jj+1] > x:
                ii = ii + 1
                jj = jj + 1


            if list2[ii][jj] > x:
                max_number = list2[ii][jj]
                list2[ii][jj] = 0


            sum_number += max_number
            #列表清零
            while max_number != 0 and  list2[ii-1][jj-1] != 0:
                list2[ii-1][jj-1] = 0
                ii = ii - 1
                jj = jj - 1

            max_number = 0
    # print(list2)
    return sum_number

#database是['123','32131','123123131']
#x是一个阈值,这个阈值的大小根据实际情况调整
#x代表含义,一样的并且长度大于x子串的都要计入其中
def get_LongSubstringSim(database,x):

    resdict_LongSubstring = {}

    for i, s in enumerate(database):
        list_i = []
        # if j == len(sqllist):
        #     break;
        for j in range(len(database)):
            list_i.append(getSimilar(s, database[j],x))

        list_i[i] = 0
        # print(list_i)
        resdict_LongSubstring[i] = list_i
        # print(reslist_simhash)

    dict_result={}

    for i in range(len(resdict_LongSubstring)):
        max = 0
        resdict_LongSubstring[i][i] = 0
        for j in range(len(resdict_LongSubstring.get(i))):

            if resdict_LongSubstring[i][j] > max :
                max = resdict_LongSubstring[i][j]
                dict_result[i] = (j,max)

    return dict_result

#5.稀疏矩阵相似度计算方法
#keyword是一个字符串,tests是一个字符串列表
#返回是一个list 第一个就是和第一个比较的结果，第二个就是和第二个比较的结果
def getSparseMatrixSimilarity(keyword,texts):

    # 1、将【文本集】生成【分词列表】
    texts = [jieba.lcut(text) for text in texts]

    # 2、基于文本集建立【词典】，并获得词典特征数
    dictionary = Dictionary(texts)
    num_features = len(dictionary.token2id)

    # 3.1、基于词典，将【分词列表集】转换成【稀疏向量集】，称作【语料库】
    corpus = [dictionary.doc2bow(text) for text in texts]
    # 3.2、同理，用【词典】把【搜索词】也转换为【稀疏向量】
    kw_vector = dictionary.doc2bow(jieba.lcut(keyword))

    # 4、创建【TF-IDF模型】，传入【语料库】来训练
    tfidf = TfidfModel(corpus)
    # 5、用训练好的【TF-IDF模型】处理【被检索文本】和【搜索词】
    tf_texts = tfidf[corpus]  # 此处将【语料库】用作【被检索文本】
    tf_kw = tfidf[kw_vector]
    # 6、相似度计算
    sparse_matrix = SparseMatrixSimilarity(tf_texts, num_features)
    similarities = sparse_matrix.get_similarities(tf_kw)
    # for e, s in enumerate(similarities, 1):
    #     print('kw 与 text%d 相似度为：%.2f' % (e, s))

    return similarities
#database同上
def get_SparseMS(database):
    resdict_SparseMS = {}

    for i in range(len(database)):
        list_i = getSparseMatrixSimilarity(database[i],database)
        list_i[i] = 0
        max = 0
        # print(list_i)

        for j in range(len(list_i)):
            if list_i[j] > max:
                max = round(list_i[j],3)
                resdict_SparseMS[i] = (j,max)
    return resdict_SparseMS

#6.通过K-gtamHash计算相似度
#主要的使用方法getKgramHashim
#获得切片
#K值切片的大小
def generateKgram(fileLine,K):

    kgram = []
    for i in range(len(fileLine)):
        if(i+K > len(fileLine)):
            break
        shingle = fileLine[i:i+K]
        kgram.append(shingle)

    return kgram
'''    
    输入：kgram-->窗口中的内容 
    输出：哈希值
    改进算法 通过公式H(c2,c3,...,ck+1) = (H(c1...ck)-c1*(b**(k-1)))*b+ck+1
'''
def generateHash1(Base,kgram,K):
    HashList = []
    hash = 0

    firstShingle = kgram[0]

    for j in range(K):
        hash += ord(firstShingle[j]) * (Base ** (K - 1 - j))

    HashList.append(hash)

    for i in range(1,len(kgram)):
        preshingle = kgram[i-1]
        shingle = kgram[i]
        hash = hash*Base - ord(preshingle[0])*(Base**K)+ord(shingle[K-1])
        HashList.append(hash)

    return HashList
#获得最小值
def getmin(list):

    mindict={}
    min = list[0]
    mindict[0] = 0
    mindict[1] = min
    for i in range(len(list)):

        if(list[i] <= min):
            min = list[i]
            mindict[0] = i
            mindict[1] = min

    return mindict
# 获得特征值
def getCvalue(WinSize,hashValues):

    # minHash = 0
    # minpos = 0
    fingerPrint = {}
    for i in range(len(hashValues)):
        if(i+WinSize > len(hashValues)):
            break

        tmplist = hashValues[i:i+WinSize]
        #print(tmplist)
        # minHash = tmplist[WinSize-1]
        # minpos = WinSize+i-1

        dict = getmin(tmplist)

        minpos = dict.get(0)+i
        minHash = dict.get(1)

        if minpos not in fingerPrint:
            fingerPrint[minpos] = minHash

    return fingerPrint
# 两个里面有重复的情况怎么办？
# mode = 1 严格 mode = 0 宽松
def getSimnumber(A,B,mode):
    list1 = A.values()
    list2 = B.values()
    number = 0
    for i in list1:
        if i in list2:
            number = number + 1

    number2 = 0
    for i in list2:
        if i in list1:
            number2 = number2 + 1

    if mode == 1:
        return max(number,number2)
    elif mode == 0:
        return min(number,number2)
    else:
        print("error")
#相似度计算公式
# 严格模式
#介绍 K值
#WindowSize
#Base直接设置成2或者任意的数值均可
#txt1以及txt2,要比较的两个文本已经去了标点符号的
#返回值是一个数
def getKgramHashim(K,WindowSize,Base,txt1,txt2):

    list1 = generateKgram(txt1, K)
    list2 = generateKgram(txt2, K)
    list_1 = generateHash1(Base, list1, K)
    list_2 = generateHash1(Base, list2, K)
    dict1 = getCvalue(WindowSize, list_1)
    dict2 = getCvalue(WindowSize, list_2)

    sum = len(dict1)+len(dict2)
    similar = round(2.0*getSimnumber(dict1,dict2,1)/sum,2)

    return similar

#整合一波

#
def get_KgramHashim(K,WindowSize,Base,database):

    dict_result = {}
    for i,s in enumerate(database):
        list_i = []
        for j in range(len(database)):
            list_i.append(getKgramHashim(K,WindowSize,Base,s,database[j]))
        list_i[i] = 0
        dict_result[i] = list_i

    # print(dict_result)
    dict_result2 = {}
    for i in range(len(dict_result)):
        max = 0

        for j in range(len(dict_result[i])):
            if dict_result[i][j] > max:
                max = dict_result[i][j]
                dict_result2[i] = (j,max)

    return dict_result2


if __name__ == '__main__':

    sql = ['月5日 Python入门之类(class) Python3 面向对象 Python从设计之初就已经是一门面向对象的语言,正因为如此,在Python中创建一个类和对象是很容易的。本章节我们将详细介...'
           ,'018年12月21日 python中class的继承 """ 继承: 实现代码的重用,相同的代码不需要重复的写 """ # 定义父类 class Animal: def eat(self): print(n(se...'
           ,'2020年3月28日 ​ 登录加入知乎 Python程序中可以没有class吗? 关注问题​写回答Python 编程 Python 入门 Python程序中可以没有class吗? Python的class看起来有些蛋疼,但是实...'
           ,'2005年8月25日 首先第一点,你会发现Class的定义中有一个括号,这是体现继承的地方。 Java用extends,C#、C++用冒号(:),Python则用括号了。从括号中包含着两个值,聪明的你一定可...'
           ]


    print(get_simhash_similarity(sql))
    print(get_LongSubstringSim(sql,5))
    print(get_SparseMS(sql))
    print(get_KgramHashim(3,4,2,sql))





