'''
import cv2

image = cv2.imread('test\ptest2.jfif')
image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
cv2.threshold(image, 200, 255, 0, image)

cv2.namedWindow("Image")
cv2.imshow("Image", image)
cv2.waitKey(0)
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

# img = cv2.imread('test.jpg')                         #这几行是对图像进行降噪处理，但事还存在一些问题。

# dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

# plt.subplot(121),plt.imshow(img)
# plt.subplot(122),plt.imshow(dst)
# plt.show()

#fn = "test\ptest5.jpg"
fn = "test\ptest3.jpg"
if __name__ == '__main__':
    print('loading %s' % fn)
    img = cv2.imread(fn)  # 读取图像 修改上方 fn的路径即可
    sp = img.shape
    print(sp)  # 在编译结果处显示图片的信息 这行没啥用

    # 获取图像大小
    sz1 = sp[0]  # 长
    sz2 = sp[1]  # 宽
    print('width:%d\nheight:%d' % (sz2, sz1))  # 控制窗口显示的比例
    # 创建一个窗口显示图像
    cv2.namedWindow('img')  # 这行没啥用 控制显示图片窗口的名字
    cv2.imshow('img', img)  # 显示图片
    # 复制图像矩阵，生成与源图像一样的图像，并显示
    myimg2 = img.copy();
    cv2.namedWindow('myimg2')  # 这行没啥用 控制显示图片窗口的名字
    cv2.imshow('myimg2', myimg2)
    # 复制并转换为灰度化图像并显示
    myimg1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度值函数
    cv2.namedWindow('myimg1')
    cv2.imshow('myimg1', myimg1)  # 显示灰度处理后的函数
    cv2.imwrite('gray.jpg', myimg1)  # 保存当前灰度值处理过后的文件
    cv2.waitKey()  # 第一个参数是保存文件的名称，必须加jgp，png等的后缀否则报错。第二个参数是保存的对象
    cv2.destroyAllWindows()
