# 搜索引擎配置
class EngineConfManage:
    def get_Engine_conf(self, engine_name):
        if engine_name == 'baidu':
            return BaiduEngineConf()
        elif engine_name == 'qihu360':
            return Qihu360EngineConf()
        elif engine_name == 'sougou':
            return SougouEngineConf()


class EngineConf:
    def __init__(self):
        self.engineConf = {}

    def get_conf(self):
        return self.engineConf


class BaiduEngineConf(EngineConf):
    engineConf = {}

    def __init__(self):
        self.engineConf['searchTextID'] = 'kw'
        self.engineConf['searchBtnID'] = 'su'
        self.engineConf['nextPageBtnID_xpath_f'] = '//*[@id="page"]/div/a[10]'
        self.engineConf['nextPageBtnID_xpath_s'] = '//*[@id="page"]/div/a[11]'
        self.engineConf['searchContentHref_class'] = 't'
        self.engineConf['website'] = 'http://www.baidu.com/'


class Qihu360EngineConf(EngineConf):
    def __init__(self):
        pass


class SougouEngineConf(EngineConf):
    def __init__(self):
        pass