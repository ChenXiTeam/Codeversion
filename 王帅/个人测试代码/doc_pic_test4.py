import docx
import os
import re


def get_pictures(word_path, result_path):
    """
    图片提取
    :param word_path: word路径
    :param result_path: 结果路径
    :return:
    """
    doc = docx.Document(word_path)
    dict_rel = doc.part._rels
    for rel in dict_rel:
        rel = dict_rel[rel]
        if "image" in rel.target_ref:
            if not os.path.exists(result_path):
                os.makedirs(result_path)
            img_name = re.findall("/(.*)", rel.target_ref)[0]
            word_name = os.path.splitext(word_path)[0]
            if os.sep in word_name:
                new_name = word_name.split('\\')[-1]
            else:
                new_name = word_name.split('/')[-1]
            img_name = f'{new_name}_{img_name}'
            with open(f'{result_path}/{img_name}', "wb") as f:
                f.write(rel.target_part.blob)

get_pictures('E:\python\py_pick\\test\\test1.docx','E:\python\py_pick\\test')