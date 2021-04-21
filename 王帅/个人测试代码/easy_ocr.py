import easyocr
import os
import time
from datetime import datetime
#cpu计算
reader = easyocr.Reader(['ch_sim','en'],False) #False为不使用GPU
starttime=datetime.now()
print('start')
#decoder 为引擎，detail 为是否显示位置信息 batch_size 设置越大，占用内存越高，识别速度越快
result = reader.readtext(image='test\ptest3.jpg',decoder='greedy',batch_size=20,detail=0)
endtime=datetime.now()
print('cpu need time',(endtime-starttime).seconds,'s')
#gpu计算
reader = easyocr.Reader(['ch_sim','en'])
starttime=datetime.now()
print('start')
result = reader.readtext(image='test.jpg',decoder='greedy',batch_size=20,detail=0)
endtime=datetime.now()
print('gpu need time',(endtime-starttime).seconds,'s')
print(result)