
import re
import chardet

# 获取文件编码格式
def get_encode(path):
  f = open(path, 'rb')
  data = f.read()
  f.close()
  encode = (chardet.detect(data))['encoding']
  return encode

def delete_node_py(in_path, out_path):
    # 暂时不考虑多行，会与字符串混淆

    bds0 = '#.*'  # 标准匹配单行注释

    target0 = re.compile(bds0)  # 单行注释

    encode = get_encode(in_path)
    if (encode == 'utf-8'):
        f = open(in_path, encoding='utf-8')
    else:
        f = open(in_path)

    data = f.read()

    result0 = target0.findall(data)

    result = []
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


in_path='E:\python\py_pick\\result\image_binarization.py'
out_path='E:\python\py_pick\\result\p.txt'
delete_node_py(in_path, out_path)