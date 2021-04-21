from Browser import BrowserManage
from Analyse import Analyse
from FileHandle import FileHandle

class Manage:
    def __init__(self,conf):
        self.drvier=BrowserManage(conf)
        self.textdic=FileHandle().get_text()
        self.analyse=Analyse()
    def get_local_analyse(self):
        resdic={}
        url_content = self.drvier.search()  # 获取搜索结果及内容
        for k in self.textdic:
            res = {}
            for k1 in url_content:
                res[k1] = self.analyse.get_Tfidf(self.textdic[k], url_content[k1])  # 逐个分析
            resdic[k] = res


        '''希望只遍历一遍网页
        for k in self.textdic:
            res={}
            self.drvier.set_kw(k)
            url_content=self.drvier.search()#获取搜索结果及内容
            for k1 in url_content:
                res[k1]=self.analyse.get_Tfidf(self.textdic[k],url_content[k1])
            resdic[k]=res
        '''

        return resdic