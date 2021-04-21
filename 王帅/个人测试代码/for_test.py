import docx
from docx import Document
import base64
import requests
import re
import os
from os.path import basename
import chardet
import fuzzywuzzy
from fuzzywuzzy import fuzz

# 判断txt中的代码类型
def txt_to_code(in_path, out_path):
    # 由于一小块代码意义不大，这里暂时考虑完整的代码
    with open(in_path, encoding="utf-8") as file:
        alltext = file.read()
        print(alltext)

        # 指针回到开头
        file.seek(0)

        # 读文本的前10个字符并打印出来
        head = file.read(10)
        print(head)

        # 部分匹配，如果S1是S2的子串依然返回100
        # 没有区分c和c++
        same_degree = []

        same_degree.append(fuzz.partial_ratio(head, '#include <iostream>'))
        same_degree.append(fuzz.partial_ratio(head, 'using namespace std;'))
        same_degree.append(fuzz.partial_ratio(head, 'package'))
        same_degree.append(fuzz.partial_ratio(head, 'public static void main'))
        same_degree.append(fuzz.partial_ratio(head, 'public void'))
        same_degree.append(fuzz.partial_ratio(head, 'int main()'))
        same_degree.append(fuzz.partial_ratio(head, 'def'))

        max_data = max(same_degree)
        max_index = same_degree.index(max(same_degree))+1

        tail = ''
        if max_index in range(1,3):
            tail = 'cpp'
        if max_index in range(3, 6):
            tail = 'java'
        if max_index in range(6, 8):
            tail = 'python'

        out_path = in_path[:-3]+tail

        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(alltext)
        f.close()
    file.close()




word_path='E:\python\py_pick\\result\ptest1.txt'
result_path='E:\python\py_pick\\result\ptest1_txt_to_code.txt'
txt_to_code(word_path, result_path)