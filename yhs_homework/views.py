from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from selenium import webdriver
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import xlrd
# Create your views here.
flag = 1


class BeautifulPicture():

    def __init__(self):  #类的初始化操作
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'}  #给请求指定一个请求头来模拟chrome浏览器
        self.web_url = 'https://edition.cnn.com/search/?q=Trump'
        #self.folder_path = 'D:\CNN_NEWs'

    def get_pic(self):
        print('开始网页get请求')

        driver = webdriver.PhantomJS()
        print('ok1')
        df = pd.DataFrame(columns=('index', 'href', 'heading', 'time'))
        mytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        df.loc[1, 'time'] = mytime
        driver.get(self.web_url)
        print('ok2')
        self.scroll_down(driver=driver, times=1)  #执行网页下拉到底部操作
        print('开始获取所有h3标签')
        page_one = BeautifulSoup(driver.page_source, 'html.parser').find_all('h3', class_='cnn-search__result-headline')  #获取网页中的搜索结果的所有h3标签


        index = 0;

        for item_in_one in page_one:
           item1 = item_in_one.a
           index += 1
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
        for item_in_two in page_two:
           item2 = item_in_two.a
           index += 1
           df.loc[index, 'index'] = index
           df.loc[index, 'href'] = item2['href'][2:]
           df.loc[index, 'heading'] = item2.contents[0]
           # print(item2['href'])
           # print(item2.contents)

        driver.find_element_by_class_name('pagination-arrow-right').click()
        self.scroll_down(driver=driver, times=1)
        page_three = BeautifulSoup(driver.page_source, 'html.parser').find_all('h3', class_='cnn-search__result-headline')
        for item_in_three in page_three:
            item3 = item_in_three.a
            index += 1
            df.loc[index, 'index'] = index
            df.loc[index, 'href'] = item3['href'][2:]
            df.loc[index, 'heading'] = item3.contents[0]
            # print(item3['href'])
            # print(item3.contents)

        #print('开始创建文件夹')
        #is_new_folder = self.mkdir(self.folder_path)
        #print('开始切换文件夹')
        #os.chdir(self.folder_path)   #切换路径至上面创建的文件夹

        print("提取的新闻数量是：", len(page_one)+len(page_two)+len(page_three))   #Check Total Number
        #file_names = self.get_files(self.folder_path)  #获取文件家中的所有文件名，类型是list
        mytime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        df.to_excel('cnn_search.xls')


    def save_img(self, url, file_name): ##保存图片
        #print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name,'图片保存成功！')
        f.close()

    def request(self, url):  #返回网页的response
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

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



def home(request):
    return render(request, 'cnn.html')


def tw(request):
    return render(request, 'twitter.html')


@csrf_exempt
def get_execl(request):
    if request.method == "POST":
        file_name = request.POST['filename']
        d = os.path.dirname(__file__) + '\\'
        print(d)
        data = xlrd.open_workbook(d + file_name)
        if os.path.exists(d + file_name):
            data = xlrd.open_workbook(d + file_name)
            table = data.sheet_by_index(0)
            nrows = table.nrows
            execlData = []
            mytime = table.cell(1, 4).value
            print(mytime)
            for row in range(1, nrows):
                c = dict([('no', int(table.cell(row, 1).value)), ('href', table.cell(row, 2).value), ('heading', table.cell(row, 3).value)])
                execlData.append(c)
            return HttpResponse(json.dumps({
                "success": 1,
                "execlData": execlData,
                "time": mytime
            }))
        else:
            return HttpResponse(json.dumps({
                "success": -1
            }))


@csrf_exempt
def get_cnn(request):
    if request.method == "GET":
        beauty = BeautifulPicture()  # 创建类的实例
        beauty.get_pic()  # 执行类中的方法
        #-----------------------------------------------------------------------
        flag = 1
        return HttpResponse(json.dumps({
            "success": 1
        }))
    return HttpResponse(json.dumps({
        "success": -1
    }))



