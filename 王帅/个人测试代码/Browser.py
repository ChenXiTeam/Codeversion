from selenium import webdriver
from bs4 import BeautifulSoup
from SearchEngine import EngineConfManage
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import hashlib
import time
import xlwt
import requests
from selenium.webdriver.firefox.options import Options

class Browser:
    def __init__(self,conf):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        self.browser = webdriver.Firefox(executable_path=r'geckodriver.exe', options=firefox_options)
        self.conf=conf
        # self.conf['kw']=''
        self.engine_conf=EngineConfManage().get_Engine_conf(conf['engine']).get_conf()
    #搜索内容设置
    def set_kw(self,kw):
        self.conf['kw']=kw
    #搜索内容写入到搜素引擎中
    def send_keyword(self):
        input = self.browser.find_element_by_id(self.engine_conf['searchTextID'])
        input.send_keys(self.conf['kw'])
    #搜索框点击
    def click_search_btn(self):
        search_btn = self.browser.find_element_by_id(self.engine_conf['searchBtnID'])
        search_btn.click()
    #获取搜索结果与文本
    def get_search_res_url(self):
        print('get_search_res_url')
        res_link={}
        WebDriverWait(self.browser,timeout=30,poll_frequency=1).until(EC.presence_of_element_located((By.ID, "page")))
        #内容通过 BeautifulSoup 解析
        content=self.browser.page_source
        soup = BeautifulSoup(content, "html.parser")
        search_res_list=soup.select('.'+self.engine_conf['searchContentHref_class'])

        while len(res_link)<self.conf['target_page']:
            for el in search_res_list:
                js = 'window.open("'+el.a['href']+'")'
                self.browser.execute_script(js)
                handle_this=self.browser.current_window_handle  #获取当前句柄
                handle_all=self.browser.window_handles          #获取所有句柄
                handle_exchange=None                            #要切换的句柄
                for handle in handle_all:                       #不匹配为新句柄
                    if handle != handle_this:                   #不等于当前句柄就交换
                        handle_exchange = handle
                self.browser.switch_to.window(handle_exchange)  #切换
                time.sleep(1)      #目前没有更好的解决方法，只能牺牲时间
                real_url=self.browser.current_url
                print(real_url)
                if real_url in self.conf['white_list']:         #白名单
                    continue
                time.sleep(1)
                res_link[real_url]=self.browser.page_source     #结果获取
                self.browser.close()
                self.browser.switch_to.window(handle_this)
            content_md5=hashlib.md5(self.browser.page_source.encode(encoding='UTF-8')).hexdigest() #md5对比
            #self.click_next_page(content_md5)    翻页方法有问题  暂时不用  这样导致target_page无效
        return res_link
    #下一页
    def click_next_page(self,md5):
        WebDriverWait(self.browser,timeout=10,poll_frequency=1).until(EC.presence_of_element_located((By.ID, "page")))
        #百度搜索引擎翻页后下一页按钮 xpath 不一致 默认非第一页xpath
        try:
            next_page_btn = self.browser.find_element_by_xpath(self.engine_conf['nextPageBtnID_xpath_s'])
        except:
            next_page_btn = self.browser.find_element_by_xpath(self.engine_conf['nextPageBtnID_xpath_f'])
        next_page_btn.click()
        #md5 进行 webpag text 对比，判断是否已翻页 （暂时使用，存在bug）
        i=0
        while md5==hashlib.md5(self.browser.page_source.encode(encoding='UTF-8')).hexdigest():#md5 对比
            time.sleep(0.3)#防止一些错误，暂时使用强制停止保持一些稳定
            i+=1
            if i>100:
                return False
        return True
class BrowserManage(Browser):
    #打开目标搜索引擎进行搜索
    def search(self):
        self.browser.get(self.engine_conf['website'])       #打开搜索引擎站点
        self.send_keyword()                                 #输入搜索kw
        self.click_search_btn()                             #点击搜索
        return self.get_search_res_url()                    #获取web页搜索数据

    
   