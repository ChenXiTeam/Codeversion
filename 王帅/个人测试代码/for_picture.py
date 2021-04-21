from PIL import Image
import pytesseract

in_path = "E:\python\py_pick\\test\ptest1.jpg"
out_path = 'E:\python\py_pick\\result\ptest1.txt'

f = open(out_path, 'w' ,encoding='utf-8')

text=pytesseract.image_to_string(Image.open(in_path), lang='chi_sim')
f.write(text)
print(text)

f.close()
