# 通过python实现最长公共子序列算法

## 前言
算法的主要思想是匹配两个文章中最长的公共子序列，进而判断两篇文章的相似度。这个代码的实现是通过双循环，所以效率上能会存在一定的缺陷。
**注明：**算法的思想的原文章，实在是找不到了，在此声明抱歉。

## 实现思想
1、首先是把字符串矩阵化“appl”和“eppl”
2、然后相同的地方（i，j）置为（i-1，j-1）+1 注意边界值。

|      | a    | p    | p    | l    |
| ---- | ---- | ---- | ---- | ---- |
| e    | 0    | 0    | 0    | 0    |
| p    | 0    | 1    | 1    | 0    |
| p    | 0    | 1    | 2    | 0    |
| l    | 0    | 0    | 0    | 3    |

3、我的代码中又改进的地方，主要就是考虑到在只考虑计算最长的那一个的公共子串的情况下，如果比较的两个文本比较大那么即便两篇是雷同的，但是公共子序列只取一个的话，最后的相似度还是会比较小，基于以上想法，改进了一下算法，设置成大于X（长度）的子序列都要计算在内。
4、改进思想，在生成完矩阵之后，原来是去找最大的值，现在则是找到大于x的值，然后沿着主对角线方向向下走，直到找到最大的，然后记录下这个值，然后反向清零，一直清到0为止。
最大的缺陷，三重循环（人傻了），应该想办法优化一下。。。。目前来看可以考虑使用三维列表，以内存换效率（木有实现，只是想想）。

## 整体代码

```python
import numpy as np
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

def getSubstring(a,b):

    number = 0
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

    max_number = 0
    for i in range(max_s):
        for j in range(max_s):
            if list2[i][j] > max_number:
                max_number = list2[i][j]

    return max_number

def getSimilar(A,B):

    a = int(getSubstring(A, B))

    similar = round( (2.0 * a ) / (len(A)+len(B)),2)
    return similar


#字符长度大于x计入
def getSubstring2(a,b,x):

    number = 0
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
            while ii+1 < max_s and jj+1 < max_s and list2[ii][jj] >= x:
                ii = ii + 1
                jj = jj + 1
                if list2[ii][jj] > list2[ii-1][jj-1]:
                    max_number = list2[ii][jj]

            sum_number += max_number
            #列表清零
            while max_number != 0 and  list2[ii-1][jj-1] != 0:
                list2[ii-1][jj-1] = 0
                ii = ii - 1
                jj = jj - 1
            max_number = 0
    # print(list2)
    return sum_number

# 另一个计算方法，大于x以上的都计入，不仅仅取最大值
#设计一个分段的，
if __name__ == '__main__':
    txt1 = getThetxt("C:/Users/60917/Desktop/第一章.txt")
    txt2 = getThetxt("C:/Users/60917/Desktop/第二章.txt")
    print(getSubstring2(txt1,txt2,11))
    # print(getSimilar(txt1,txt2))
    # print(getSubstring2("a213pple","a1244pple",2))
```

