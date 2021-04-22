import requests
import json

from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth


# 获得项目的bug
def getBugs():
    init_resopnse = requests.post(
        "http://localhost:9000/api/issues/search?componentKeys=" + project_name + "&types=BUG", auth=auth)
    init_text = init_resopnse.text
    init_json_text = json.loads(init_text)
    total = int(init_json_text['total'])
    pageNum = total // 100
    for p in range(1, pageNum + 2):
        resopnse = requests.post(
            "http://localhost:9000/api/issues/search?componentKeys=" + project_name + "&types=BUG&p=" + str(
                p), auth=auth)
        text = resopnse.text
        json_text = json.loads(text)
        for i in range(len(json_text['issues'])):
            print(json_text['issues'][i]['component'] + '      ', end="")
            print("line:" + str(json_text['issues'][i]['line']) + '     ', end="")
            print(json_text['issues'][i]['message'])


# 获得项目的异味(已筛选出严重的 和 阻断的）
def getCodeSmell():
    init_resopnse = requests.post(
        "http://localhost:9000/api/issues/search?componentKeys=" + project_name + "&types=CODE_SMELL&severities=CRITICAL,BLOCKER",
        auth=auth)
    init_text = init_resopnse.text
    init_json_text = json.loads(init_text)
    total = int(init_json_text['total'])
    pageNum = total // 100
    for p in range(1, pageNum + 2):
        resopnse = requests.post(
            "http://localhost:9000/api/issues/search?componentKeys=" + project_name + "&types=CODE_SMELL&severities=CRITICAL,BLOCKER&p=" + str(
                p), auth=auth)
        text = resopnse.text
        json_text = json.loads(text)
        for i in range(len(json_text['issues'])):
            print(json_text['issues'][i]['component'] + '      ', end="")
            print("line:" + str(json_text['issues'][i]['line']) + '     ', end="")
            print(json_text['issues'][i]['message'])



if __name__ == "__main__":
    project_name = input("请输入项目名称：")
    auth = HTTPBasicAuth("admin".encode('utf-8'), "admin1")
    getCodeSmell()
    result_type = input("请选择要检测的类型（BUG or CODE_SMELL or VULNERABILITY）")
    if result_type == 'BUG':
        getBugs()
    elif result_type == 'CODE_SMELL':
        getCodeSmell()
    else:
        print("输入错误")
