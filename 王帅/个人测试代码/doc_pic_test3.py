import os

for file in os.listdir('E:\python\py_pick\\test'):
    try:
        # 跳过非docx文件
        if ".docx" not in file:
            continue
        # 创建imgPath
        subImgPath = imgPath + re.sub(".docx", "", file)
        if not os.path.exists(subImgPath):
            os.makedirs(subImgPath)

        doc = docx.Document(filePath + file)  # 打开文件
        for rel in doc.part._rels:
            rel = doc.part._rels[rel]  # 获得资源
            if "image" not in rel.target_ref:
                continue
            imgName = re.findall("/(.*)", rel.target_ref)[0]
            with open(subImgPath + "/" + imgName, "wb") as f:
                f.write(rel.target_part.blob)
        UI.currentFile.setText("当前文件：" + imgName)
    except:
        continue