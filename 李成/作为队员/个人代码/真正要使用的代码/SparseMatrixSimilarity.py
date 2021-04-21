import jieba
import gensim
#标点符合去掉
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

#分词
def getWordFromList(str):
    words = []
    for sentence in str:
        sentence_list = [word for word in jieba.cut(sentence)]
        words.append(sentence_list)
    return words

def getSparseMatrixSimilarity(t,mysql):
    mysql_list = getWordFromList(mysql)
    dictionary = gensim.corpora.Dictionary(mysql_list)

    corpus = [dictionary.doc2bow(doc) for doc in mysql_list]
    # print(corpus)
    t_list = [word for word in jieba.cut(t)]

    test_doc_vec = dictionary.doc2bow(t_list)
    tfidf = gensim.models.TfidfModel(corpus)
    index = gensim.similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))

    sim = index[tfidf[test_doc_vec]]
    return sim




if __name__ == '__main__':

    first = 'C:/Users/60917/Desktop/第一章.txt'
    second = 'C:/Users/60917/Desktop/第二章.txt'
    third = 'C:/Users/60917/Desktop/第三章.txt'
    #获得字符串
    f = getThetxt(first)
    s = getThetxt(second)
    t = getThetxt(third)
    #将前两个模拟数据库
    mysql = [f,s]
    print(getSparseMatrixSimilarity(t,mysql))
 #   t1 = jieba.cut(t)


