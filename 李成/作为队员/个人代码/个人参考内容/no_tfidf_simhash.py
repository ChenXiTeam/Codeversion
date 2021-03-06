import codecs
#有待改进

import jieba
import numpy as np
import jieba.posseg as pseg
import jieba.analyse

class simhash:
    def __init__(self,content):
        self.simhash=self.simhash(content)
    def __str__(self):
        return str(self.simhash)

    def simhash(self,content):
        seg = jieba.cut(content)
        jieba.analyse.set_stop_words('C:/Users/60917/Desktop/StopWords.txt')
        keyWord = jieba.analyse.extract_tags('|'.join(seg), topK=20, withWeight=True, allowPOS=())  # 在这里对jieba的tfidf.py进行了修改
        # 将tags = sorted(freq.items(), key=itemgetter(1), reverse=True)修改成tags = sorted(freq.items(), key=itemgetter(1,0), reverse=True)
        # 即先按照权重排序，再按照词排序
        keyList = []
        # print(keyWord)
        for feature, weight in keyWord:
            weight = int(weight * 20)
            feature = self.string_hash(feature)
            temp = []
            for i in feature:
                if (i == '1'):
                    temp.append(weight)
                else:
                    temp.append(-weight)
            # print(temp)
            keyList.append(temp)
        list1 = np.sum(np.array(keyList), axis=0)
        print(list1)
        if (keyList == []):  # 编码读不出来
            return '00'
        simhash = ''
        for i in list1:
            if (i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash

    def hammingDis(self, com):
        t1 = '0b' + self.simhash
        t2 = '0b' + com.simhash
        n = int(t1, 2) ^ int(t2, 2)
        i = 0
        while n:
            n &= (n - 1)
            i += 1
        return i

# hash算法
    def string_hash(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            print(source, x)

            return str(x)


if __name__ == '__main__':
    # print(simhash("我是王帅，我爱英语"))
    print("***")
    print(simhash.hammingDis(simhash("我是王帅，我爱英语"),simhash("我是李成，我爱数学")))
