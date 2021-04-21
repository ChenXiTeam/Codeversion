# 基于Winnowing的代码相似度算法

## 前言

本文的设计思想以及算法的使用都是基于以下两篇文章。

《Winnowing: Local Algorithms for Document Fingerprinting》

《程序代码相似度度量算法研究_邓爱萍》

相关实现过程参考https://blog.csdn.net/chichoxian/article/details/53128303，文章幽默诙谐，深入浅出，建议大家去看一下。

但是这里提一下，他的文章没有实现相似度的计算问题，我在邓爱萍的文章挑选了一种算法，最后实验了相似度的计算问题。

## 算法的思路

《Winnowing: Local Algorithms for Document Fingerprinting》在这篇文章中介绍了一种算法，在下面简单的介绍一下。

### 首先是关键字的提取

无论是代码相似度的比较还是文本相似度的比较（我这里是代码相似度），我们都需要找到文章中的关键字。所以第一步是关键字的提取。

PS：这里只讲实现过程，关于论证这样做的准确性以及正确性的论证可以参见原文。

1、首先看这样一个字符串“yabbadabbadoo”，确定gram的大小，这里用K来表示，K，gram的具体含义参见下图（文章我都白嫖了，盗个图不过分吧/狗头保命）

![image-20210411103813025](C:\Users\60917\AppData\Roaming\Typora\typora-user-images\image-20210411103813025.png)

这里的红色蓝色绿色的，就是gram，在这里的K值就是3，可以记作3-gram

2、于是乎，我们获得了以下的子串

“yab”，“abb”，“bba”，“bad”，“ada”，”dab“，”abb“,”bba“，”bad“，”ado“，”doo“

可以计算我们获得的        子串个数 = 原字符串长度 - K + 1

所以这里可以看出，这种选择方案其实对文档的压缩并不明显，甚至效果很差，所以我们决定进一步压缩。

PS：这里的压缩值得是关键字的提取。

3、所以在以上子串中我们决定选择一种比较常见的方法进行筛选，然后获得其中代表作为文章的关键字

（1）首先对每一个子串hash我们可以得到一列数.所以有必要说一下我们所采用的hash函数。下图

![image-20210411105950384](C:\Users\60917\AppData\Roaming\Typora\typora-user-images\image-20210411105950384.png)

看不懂？没关系，下面有解释

第一个红框代表我们所使用的hash函数，第二个红框就是优化。通过H（K）来求H（K+1），不用重复计算了。这里的ci表示字符串中的第i个字符的ASCII值，b表示一个基数（BASE）这里我们可以取其为2（不确定是不是可以随便取），然后就可以计算出数了。

对应后面的函数def generateHash(Base,kgram,K)【未优化】 和def generateHash1(Base,kgram,K)【优化】

这里贴以下计算结果

![image-20210411110546611](C:\Users\60917\AppData\Roaming\Typora\typora-user-images\image-20210411110546611.png)

可以看出相同的值，hash也是相同的（第四个与倒数第三个），通过对比hash值我们来确定有没有相似。但是也可以看到第三个和第5个虽然字符串不一样，但是hash值却相同，主要原因是发生了hash碰撞，具体可以百度一下这个关键字，去理解一下hash碰撞。

（2）获得hash值之后，一种算法是通过0modp来进行选择如下：

”5“ ”10“ ”21“ ”41“ ”62“ ”26“ ”74“ ”21“

我们的p取5，所以这里选出的值就是”5“，”10“来代表这篇文章，这里我们可以容易的看出，这种选择方法有一定的缺陷，就是没办法考虑的全篇，一般文章的辨识度都在文中，只看开头一小部分是不行的（虽然上面的数据是我故意设计的）

另一种就是论文中提到的方法，通过一个滑动的窗口获得特征值我们，我们这是窗口的大小为4然后可以得到

原hashlist长度-winSize+1个小的窗口。（就是一个4个大小的窗口向右侧滑动，每次滑动一位，每滑动一次都要记录下来）

![image-20210411111852650](C:\Users\60917\AppData\Roaming\Typora\typora-user-images\image-20210411111852650.png)



得到这些小的窗口之后，我们根据以下规则进行选择。（选择最小的值，如果有两个那么就选择右侧的）

![image-20210411112136505](C:\Users\60917\AppData\Roaming\Typora\typora-user-images\image-20210411112136505.png)

获得结果：

[776, **682**, 685, 686]
[**682**, 685, 686, 685]
[685, 686, **685**, 692]
[686, 685, 692, **682**]
[685, 692, **682**, 685]
[692, **682**, 685, 686]
[**682**, 685, 686, 699]
[**685**, 686, 699, 733]

不难看出4-7行的的682其实是一个，不过他占了很多窗口的最小值。

于是我们选择除了这篇文章的特征值（计算机喜欢从0开始）

![image-20210411113317782](C:\Users\60917\AppData\Roaming\Typora\typora-user-images\image-20210411113317782.png)

至此我们文章的关键字的提取告一段落。

**可能有人会问关于K以及winSize的值的选取，这两个值的选取，要根据实际情况来进行选择，K值的选取将小于K长度的值筛选掉了，如果在英文中比如K=4，”the“就不会在统计范围内，要想做的比别人的好，这种阈值的设置就要符合自己的实际情况，可以通过做一个图表来分析阈值的取值在什么情况下比较合适。**

（PS：这样做法的正确性参见上述论文）

## 然后就是通过关键字进行相似度的分析

![image-20210411114119934](C:\Users\60917\AppData\Roaming\Typora\typora-user-images\image-20210411114119934.png)

这个是基于邓爱萍的文章中提出的一个计算方法。比较简单。

# 代码部分
```python

#先使用文本进行测试
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
    # print(d1)
    return d1


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

#获得哈希值
# 通过公式cj*(b**(k-j))
def generateHash(Base,kgram,K):
    HashList = []
    for i in range(len(kgram)):
        hash = 0
        shingle = kgram[i]

        for j in range(K):
            hash += ord(shingle[j])*(Base**(K-1-j))

        HashList.append(hash)

    return HashList

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

    minHash = 0
    minpos = 0
    fingerPrint = {}
    for i in range(len(hashValues)):
        if(i+WinSize > len(hashValues)):
            break

        tmplist = hashValues[i:i+WinSize]
        print(tmplist)
        # minHash = tmplist[WinSize-1]
        # minpos = WinSize+i-1

        dict = getmin(tmplist)

        minpos = dict.get(0)+i
        minHash = dict.get(1)

        if minpos not in fingerPrint:
            fingerPrint[minpos] = minHash

    return fingerPrint

#相似度计算公式
# 严格模式
def sim(A,B):
    sum = len(A)+len(B)
    similar = round(2.0*getSimnumber(A,B,1)/sum,2)

    return similar

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

if __name__ == '__main__':

    # hashValues = [77, 74, 42, 17, 98, 50, 17, 98, 8, 88, 67, 39, 77, 74, 42, 17, 98]
    #
    # print(getCvalue(4,hashValues))


    # txt1 = getThetxt("C:/Users/60917/Desktop/第一章.txt")
    # txt2 = getThetxt("C:/Users/60917/Desktop/第二章.txt")
    K = 3
    WindowsSize = 4
    # list1 = generateKgram(txt1, K)
    # list2 = generateKgram(txt2, K)
    # list_1 = generateHash1(2,list1,K)
    # list_2 = generateHash1(2,list2,K)
    # dict1 =  getCvalue(WindowsSize, list_1)
    # dict2 = getCvalue(WindowsSize, list_2)
    #
    # print(sim(dict1,dict2))
    list2 = generateKgram("yabbadabbadoo",K)
    print(list2)
    list3 = generateHash1(2,list2,K)
    print(list3)
    list4 = getCvalue(WindowsSize, list3)
    print(list4)



```







