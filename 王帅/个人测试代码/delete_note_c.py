
#读取字符
# c,java都可

import re
import chardet

inpath = 'E:\python\py_pick\\result\我是java.java'
outpath = 'E:\python\py_pick\\result\zz2.txt'

# 获取文件编码格式
def get_encode(path):
  f = open(path, 'rb')
  data = f.read()
  f.close()
  encode = (chardet.detect(data))['encoding']
  return encode

# 去掉c中的注释和空行
def make_to_string(inpath, outpath):
  bds0 = '//.*'  # 标准匹配单行注释
  bds1 = '\/\*(?:[^\*]|\*+[^\/\*])*\*+\/'  # 标准匹配多行注释  可匹配跨行注释

  target0 = re.compile(bds0)  # 单行注释
  target = re.compile(bds1)  # 编译正则表达式

  encode = get_encode(inpath)
  if(encode=='utf-8'):
    f = open(inpath, encoding='utf-8')
  else:
    f = open(inpath)

  data = f.read()

  result0 = target0.findall(data)

  result = target.findall(data)

  result += result0
  for i in result:
    data = data.replace(i, '')  # 替换为空字符串

  st = list(data)

  # 去掉空格一行换行
  for i in range(0, len(st)):
    for line in st:
      if '\n' in line:
        index = st.index(line)
        del st[index]
      if ' ' in line:
        index = st.index(line)
        del st[index]
      if '\t' in line:
        index = st.index(line)
        del st[index]
    mn = "".join(st)

  file = open(outpath, 'w', encoding='utf-8')
  file.write(mn)
  file.close()

make_to_string(inpath, outpath)