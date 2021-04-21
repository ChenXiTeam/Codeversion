#代码相似度，k-gramHasH算法，可用
#存在继续优化的可能性

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


    txt1 = getThetxt("C:/Users/60917/Desktop/第一章.txt")
    txt2 = getThetxt("C:/Users/60917/Desktop/第二章.txt")
    K = 3
    WindowsSize = 4
    list1 = generateKgram(txt1, K)
    list2 = generateKgram(txt2, K)
    list_1 = generateHash1(2,list1,K)
    list_2 = generateHash1(2,list2,K)
    dict1 =  getCvalue(WindowsSize, list_1)
    dict2 = getCvalue(WindowsSize, list_2)

    print(sim(dict1,dict2))