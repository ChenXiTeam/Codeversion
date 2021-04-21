from zipfile import ZipFile
from os. path import basename
zf= ZipFile('test1.docx')
for item in zf.filelist:
    t=1
    name = 'pic'+ str(t)
    t=t+1
#文件名,例如word/media/image11.jpeg
    with open(name, 'wb') as fp:
        fp.write(item.filename)

'''fn=item.filename
    if fn. endswith(('.jpg', '.jpeg', ' png')):
        print(fn)
     #读取压缩文件中图片文件的数据,写入本地文件
        with open(basename(fn), 'wb') as fp:
             fp. write(zf. read(fn))'''
