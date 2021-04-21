import math
from collections import Counter

import jieba
#标点符合去掉
excludes = {'，','。','/','《','》','？','；','‘','：','“','【','】','{','}',
            '、','|','！','@','#','￥','%','……','&','*','（','）','-','=',
            '——','+','·','~','”',
            ',','.','/','<','>','?',';','\'',':','"','[',']','{','}','\\','|',
            '~','`','!','@','#','$','%','^','&','*','(',')','_','-','+','=',
            ' ','\n'}

# tfidf 算法
def tf(word,count):
    return count[word]/sum(count.values())

def n_containing(word,count_list):
    return sum(1 for count in count_list if word in count)

def idf(word,count_list):
    return math.log10(len(count_list)/(1+n_containing(word,count_list)))

def tfidf(word,count,count_list):
    return tf(word,count)*idf(word,count_list)

def getThetxt(str):
    d1 = open(str,encoding='utf-8').read()

    for word in excludes:
        d1 = d1.replace(word,'')
    #print(d1)
    return d1

#数据处理，将字符串分词
def dataprocess(data):
    sentence_list = [word for word in jieba.cut(data)]
    count = Counter(sentence_list)
    return count

#计算数据库中第location+1的TFIDF
# location 是int database 是list [获得字符串,去掉标点，尚未分词]
def getTheTFIDF(location,database):

    if location>=len(database):
        print("location is wrong!")
        return ;

    wordlist = []
    for data in database :
        wordlist.append(dataprocess(data))

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
            # for word, score in sorted_words[:10]:
            #     print('\tWord:{},TF-IDF:{}'.format(word, round(score, 5)))
            return sorted_words;

def main():
    first = 'C:/Users/60917/Desktop/第一章.txt'
    second = 'C:/Users/60917/Desktop/第二章.txt'
    third = 'C:/Users/60917/Desktop/第三章.txt'
    # 获得字符串,去掉标点，尚未分词
    f = getThetxt(first)
    s = getThetxt(second)
    t = getThetxt(third)
    # print(f)
    database = [f,s,t]
    getTheTFIDF(1,database)

if __name__ == '__main__':
    main()