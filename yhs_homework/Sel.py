﻿from selenium import webdriver
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time


class CNN_News():

    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://edition.cnn.com/search/?q=Trump'
        #self.folder_path = 'D:\CNN_NEWs'

    def get_news(self):
        print('Starting')

        driver = webdriver.PhantomJS()
        #print('ok1')
        df = pd.DataFrame(columns=('index', 'href', 'heading', 'time'))
        mytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        df.loc[1, 'time'] = mytime
        driver.get(self.web_url)
        #print('ok2')
        self.scroll_down(driver=driver, times=1)  #执行网页下拉到底部操作
        print('Gathering all h3 tag')
        page_one = BeautifulSoup(driver.page_source, 'html.parser').find_all('h3', class_='cnn-search__result-headline')  #获取网页中的搜索结果的所有h3标签


        index = 0;
        # Extracting News in page one
        for item_in_one in page_one:
           item1 = item_in_one.a
           index += 1
           #Put into execl
           df.loc[index, 'index'] = index
           df.loc[index, 'href'] = item1['href'][2:]
           df.loc[index, 'heading'] = item1.contents[0]
           #print(item1['href'])
           #print(item1.contents)

        #driver.switch_to_frame(1)
        #print(driver.find_element_by_class_name('icon icon--arrow-right'))
        driver.find_element_by_class_name('pagination-arrow-right').click()
        self.scroll_down(driver=driver, times=1)
        page_two = BeautifulSoup(driver.page_source, 'html.parser').find_all('h3', class_='cnn-search__result-headline')
        # Extracting News in page two
        for item_in_two in page_two:
           item2 = item_in_two.a
           index += 1
           # Put into execl
           df.loc[index, 'index'] = index
           df.loc[index, 'href'] = item2['href'][2:]
           df.loc[index, 'heading'] = item2.contents[0]
           # print(item2['href'])
           # print(item2.contents)

        driver.find_element_by_class_name('pagination-arrow-right').click()
        self.scroll_down(driver=driver, times=1)
        page_three = BeautifulSoup(driver.page_source, 'html.parser').find_all('h3', class_='cnn-search__result-headline')
        # Extracting News in page three
        for item_in_three in page_three:
            item3 = item_in_three.a
            index += 1
            # Put into execl
            df.loc[index, 'index'] = index
            df.loc[index, 'href'] = item3['href'][2:]
            df.loc[index, 'heading'] = item3.contents[0]
            # print(item3['href'])
            # print(item3.contents)

        #print('开始创建文件夹')
        #is_new_folder = self.mkdir(self.folder_path)
        #print('开始切换文件夹')
        #os.chdir(self.folder_path)   #切换路径至上面创建的文件夹

        print("The total number of extracted News: ", len(page_one)+len(page_two)+len(page_three))   #Check Total Number
        #file_names = self.get_files(self.folder_path)  #获取文件家中的所有文件名，类型是list

        df.to_excel('/py/back/yhs_homework/cnn_search.xls')


    def scroll_down(self, driver, times):
        print('ok3')
        for i in range(times):
            print("Page ", str(i + 1)," Starting")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #执行JavaScript实现网页下拉倒底部
            print("Page ", str(i + 1), " Done")
            print("Page ", str(i + 1), " Loading")
            time.sleep(20)  # 等待30秒，页面加载出来再执行下拉操作

    def get_files(self, path):
        pic_names = os.listdir(path)
        return pic_names

beauty = CNN_News()  #创建类的实例
beauty.get_news()  #执行类中的方法