import chardet
path = "E:\python\py_pick\\result\众智实验二.cpp"

def get_encode(path):
    f = open(path, 'rb')
    data = f.read()
    f.close()
    encode = (chardet.detect(data))['encoding']
    return encode

print(get_encode(path))