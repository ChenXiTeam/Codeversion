import re
import chardet

def get_encode(path):
  f = open(path, 'rb')
  data = f.read()
  f.close()
  encode = (chardet.detect(data))['encoding']
  return encode

# 去掉代码中的注释和空行
def make_to_string(in_path, out_path):

  if in_path.split('.')[-1] == 'py':
      bds = '#.*'
      target = re.compile(bds)  # 单行注释
      encode = get_encode(in_path)

      if (encode == 'utf-8'):
          f = open(in_path, encoding='utf-8')
      else:
          f = open(in_path)

      data = f.read()

      result0 = target.findall(data)

      result = []
      result += result0
      for i in result:
          data = data.replace(i, '')  # 替换为空字符串

      st = list(data)


  elif in_path.split('.')[-1] == 'c' or in_path.split('.')[-1] == 'cpp' or in_path.split('.')[-1] == 'java':
      bds0 = '//.*'  # 标准匹配单行注释
      bds1 = '\/\*(?:[^\*]|\*+[^\/\*])*\*+\/'  # 标准匹配多行注释  可匹配跨行注释
      target0 = re.compile(bds0)  # 单行注释
      target = re.compile(bds1)  # 编译正则表达式
      encode = get_encode(in_path)

      if (encode == 'utf-8'):
          f = open(in_path, encoding='utf-8')
      else:
          f = open(in_path)

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

  file = open(out_path, 'w', encoding='utf-8')
  file.write(mn)
  file.close()


in_path='E:\python\py_pick\\result\众智实验二.cpp'
out_path='E:\python\py_pick\\result\z.txt'

make_to_string(in_path, out_path)