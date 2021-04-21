from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options

firefox_options = Options()
firefox_options.add_argument('--headless')

driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=firefox_options)

print(type(driver))

url='https://www.baidu.com/'

driver.get(url)

input=driver.find_element_by_id('kw')
input.send_keys('山东大学数据结构实验')
search_btn=driver.find_element_by_id('su')
search_btn.click()

time.sleep(2)  # 在此等待 使浏览器解析并渲染到浏览器

html = driver.page_source  # 获取网页内容
soup = BeautifulSoup(html, "html.parser")
search_res_list = soup.select('.t')
'''
driver.close()
import requests
rlist = []
for el in search_res_list:
    url = el.a['href']
    r = requests.get(url, timeout=(3,7))
    print(r.url)
    rlist.append(r.url)
print('done')
'''
real_url_list = []
for el in search_res_list:
    js = 'window.open("' + el.a['href'] + '")'
    print(js)
    driver.execute_script(js)
    handle_this = driver.current_window_handle  # 获取当前句柄
    handle_all = driver.window_handles  # 获取所有句柄
    handle_exchange = None  # 要切换的句柄
    for handle in handle_all:  # 不匹配为新句柄
        if handle != handle_this:  # 不等于当前句柄就交换
            handle_exchange = handle
    driver.switch_to.window(handle_exchange)  # 切换
    time.sleep(1)
    real_url = driver.current_url
    print(real_url)
    real_url_list.append(real_url)  # 存储结果
    driver.close()
    driver.switch_to.window(handle_this)

