#通过tfidf-稀疏向量计算相似度
#我记的有更好的实现
import jieba
import gensim

def getWordsFromList(str):
    words = []
    for sentence in str:
        sentence_list = [word for word in jieba.cut(sentence)]
        words.append(sentence_list)
    return words

string = ['我是李成，大家好','我是牛翔宇，大家下午好。']

#print("#")
#print(jieba.user_word_tag_tab)

tests_list = getWordsFromList(string)

dictionary = gensim.corpora.Dictionary(tests_list)

#print(dictionary)
#单词与编号之间的映射关系
#print(dictionary.token2id)

# 简单地对每个不同单词的出现次数进行了计数，并将单词转换为其编号，
# 然后以稀疏向量的形式返回结果。
corpus = [dictionary.doc2bow(doc) for doc in tests_list]
#print(corpus)

test_string2 = '李成牛翔宇'

test_doc_list = [word for word in jieba.cut(test_string2)]

print(test_doc_list)
test_doc_vec = dictionary.doc2bow(test_doc_list)

#使用TF-IDF模型对语料库建模
tfidf = gensim.models.TfidfModel(corpus)
#分析测试文档与已经存在的每个训练文本的相似程度
#通过token2id得到特征数（字典里面的键的个数）
index = gensim.similarities.SparseMatrixSimilarity(tfidf[corpus],num_features=len(dictionary.keys()))
#通过tfidf和要对比的文本的稀疏向量计算相似度
sim = index[tfidf[test_doc_vec]]
print(sim)

