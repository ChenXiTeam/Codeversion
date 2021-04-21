#通过tfidf-稀疏向量计算相似度
#我记的有更好的实现
import jieba
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import SparseMatrixSimilarity


def getWordsFromList(str):
    words = []
    for sentence in str:
        sentence_list = [word for word in jieba.cut(sentence)]
        words.append(sentence_list)
    return words

#keyword是一个字符串,tests是一个字符串列表
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
    for e, s in enumerate(similarities, 1):
        print('kw 与 text%d 相似度为：%.2f' % (e, s))

    print(sparse_matrix)
    print(similarities)

if __name__ == '__main__':

    # 文本集和搜索词
    texts = ['吃鸡这里所谓的吃鸡并不是真的吃鸡，也不是谐音词刺激的意思',
             '而是出自策略射击游戏《绝地求生：大逃杀》里的台词',
             '我吃鸡翅，你吃鸡腿']
    keyword = '玩过吃鸡？今晚一起吃鸡'

    getSparseMatrixSimilarity(keyword, texts)
