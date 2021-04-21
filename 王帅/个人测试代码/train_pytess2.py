## test.py
import os
import pytesseract
from PIL import Image
from collections import defaultdict

# tesseract.exe所在的文件路径
pytesseract.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract.exe'


# 获取图片中像素点数量最多的像素
def get_threshold(image):
    pixel_dict = defaultdict(int)

    # 像素及该像素出现次数的字典
    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            pixel_dict[pixel] += 1

    count_max = max(pixel_dict.values())  # 获取像素出现出多的次数
    pixel_dict_reverse = {v: k for k, v in pixel_dict.items()}
    threshold = pixel_dict_reverse[count_max]  # 获取出现次数最多的像素点

    return threshold




'''

def main():
    # 识别指定文件目录下的图片
    # 图片存放目录figures
    dir = 'E://python\py_pick\\test'

    correct_count = 0  # 图片总数
    total_count = 0  # 识别正确的图片数量

    # 遍历figures下的png,jpg文件
    for file in os.listdir(dir):
        if file.endswith('.png') or file.endswith('.jpg'):
            # print(file)
            image_path = '%s/%s' % (dir, file)  # 图片路径

            text = pytesseract.image_to_string(image_path)

            print(text)
'''

from urllib import *
import cv2
import io

image = Image.open('E:\python\py_pick\\test\ptest1.jpg')  # 打开图片文件
imgry = image.convert('L')  # 转化为灰度图

#image = cv2.imread('E:\python\py_pick\\test\ptest1.jpg')
#image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

cv2.threshold(image, get_threshold(imgry), 255, 0, image)

cv2.namedWindow("Image")
cv2.imshow("Image", image)



main()
