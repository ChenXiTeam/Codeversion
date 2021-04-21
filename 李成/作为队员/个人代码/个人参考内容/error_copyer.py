#汉明距离，需要调试

import codecs
import numpy as np
import jieba.posseg as pseg

def load_stopwords(path):
    return set([line.strip() for line in open(path, "r", encoding="utf-8").readlines() if line.strip()])

stopwords = load_stopwords(path='C:/Users/60917/Desktop/StopWords.txt')

def string_hash(source):
    if not source:
        return 0

    x = ord(source[0]) <7
    m = 1000003
    mask = 2 ** 128 - 1
    for c in source:
        x = ((x * m) ^ ord(c)) & mask
    x ^= len(source)
    if x == -1:
        x = -2
    x = bin(x).replace('0b', '').zfill(64)[-64:]
    return str(x)


def load_idf(path):
    words_idf = dict()
    with codecs.open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split('\t')
            if len(parts) != 2:
                continue
            if parts[0] not in words_idf:
                words_idf[parts[0]] = float(parts[1])

    return words_idf


words_idf = load_idf(path='C:/Users/60917/Desktop/idf.txt')


def compute_tfidf(text):
    words_freq = dict()
    words = pseg.lcut(text)
    for w in words:
        if w.word in stopwords:
            continue
        if w.word not in words_freq:
            words_freq[w.word] = 1
        else:
            words_freq[w.word] += 1

    text_total_words = sum(list(words_freq.values()))

    words_tfidf = dict()
    for word, freq in words_freq.items():
        if word not in words_idf:
            continue
        else:
            tfidf = words_idf[word] * (freq / text_total_words)
            words_tfidf[word] = tfidf

    return words_tfidf


def get_keywords(text, topk):
    words_tfidf = compute_tfidf(text)
    words_tfidf_sorted = sorted(words_tfidf.items(), key=lambda x: x[1], reverse=True)
    return [item[0] for item in words_tfidf_sorted[:topk]]


def hamming_distance(simhash1, simhash2):
    ham = [s1 == s2 for (s1, s2) in zip(simhash1, simhash2)]
    return ham.count(False)


def text_simhash(text):
    total_sum = np.array([0 for _ in range(64)])
    keywords = get_keywords(text, topk=2)
    for keyword in keywords:
        v = int(words_idf[keyword])
        hash_code = string_hash(keyword)
        decode_vec = [v if hc == '1' else -v for hc in hash_code]
        total_sum += np.array(decode_vec)
    simhash_code = [1 if t > 0 else 0 for t in total_sum]
    return simhash_code


def simhash_similarity(text1, text2):
    simhash_code1 = text_simhash(text1)
    simhash_code2 = text_simhash(text2)
    #print(simhash_code1, simhash_code2)
    return hamming_distance(simhash_code1, simhash_code2)


if __name__ == '__main__':
    print(simhash_similarity('在历史上有著许多数学发现', '在历史上有著许多数学发现'))