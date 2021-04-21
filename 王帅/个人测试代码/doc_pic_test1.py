from os. path import basename
from docx import Document


doc= Document('test1.docx')
for shape in doc.inline_shapes:
    contentID= shape._inline.graphic.graphicData.pic.blipFill.blip.embed
    contentType=doc.part.related_parts[contentID].content_type
    if not contentType.startswith('image'):
        continue
    imgName=basename(doc.part.related_parts[contentID].partname)
    imgData=doc.part.related_parts[contentID]._blob
    with open(imgName,'wb') as fp:
       fp. write(imgData)
