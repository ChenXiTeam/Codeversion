#读取字符
import re

inpath = 'E:\python\py_pick\\result\MagazineList.java'
outpath = 'E:\python\py_pick\\result\j.txt'

# 去掉c中的注释和空行
def make_to_string(inpath, outpath):
  bds0 = '//.*'  # 标准匹配单行注释
  bds1 = '\/\*(?:[^\*]|\*+[^\/\*])*\*+\/'  # 标准匹配多行注释  可匹配跨行注释

  target0 = re.compile(bds0)  # 单行注释
  target = re.compile(bds1)  # 编译正则表达式

  f = open(inpath,encoding='utf-8')  # 注意  有中文的时候一定要定义编码encoding  不然会报错
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
  file.write("java"+mn)
  file.close()

make_to_string(inpath, outpath)