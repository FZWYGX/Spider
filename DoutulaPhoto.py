# encoding:utf-8
import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import threading


class DouTuLaSpider:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
        # 创建Queue队列, url队列, 网页源码队列, 图片链接队列
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.img_queue = Queue()
        # photo的原始url
        self.base_url = 'http://www.doutula.com/photo/list/?page={}'

    def get_url_list(self):
        # 构造翻页链接
        for x in range(1, 100):
            url = self.base_url.format(x)
            # 放入每一页的url
            self.url_queue.put(url)

    def parse_url(self):
        while True:
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers=self.headers)
            # 得到html源码
            self.html_queue.put(response.text)

            self.url_queue.task_done()

    def parse_page(self):
        while True:
            # 去除html源码
            html_str = self.html_queue.get()
            # 解析源码
            html = etree.HTML(html_str)
            # 提取每一页表情的urls, 不提取gif动画
            imgs = html.xpath("//div[@class='page-content text-center']//img[@class!='gif']")
            for img in imgs:
                # 得到图片的链接
                img_url = img.get('data-original')
                # 得到图片的名字
                img_name = img.get('alt')
                # 替换掉文件名不能识别的字符
                img_name = re.sub(r'[\?？\.。\,，!\*\/]', '', img_name)
                # 提取后缀
                suffix = os.path.splitext(img_url)[1]
                # 替换后缀多余部分
                suffix = re.sub(r'[!dta]', '', suffix)
                # 拼接完整的名字
                filename = img_name + suffix
                print(suffix)
                # 存进img图片队列
                self.img_queue.put((img_url, filename))

            self.html_queue.task_done()

    def download_picture(self):
        while True:
            img_url, filename = self.img_queue.get()
            # 通过urllib模块下的request.urlretrieve方法, 完成图片下载
            request.urlretrieve(img_url, './images/' + filename)
            print(filename, "下载完成!")

            self.img_queue.task_done()

    def run(self):
        """
        实现主要逻辑
        """

        thread_list = []

        # 1.url_list
        thread_url = threading.Thread(target=self.get_url_list)
        thread_list.append(thread_url)

        # 2.遍历，发送请求，获取响应
        for i in range(2):
            thread_parse = threading.Thread(target=self.parse_url)
            thread_list.append(thread_parse)

        # 3.提取数据
        for i in range(2):
            thread_html = threading.Thread(target=self.parse_page)
            thread_list.append(thread_html)

        # 4.保存
        for i in range(4):
            thread_save = threading.Thread(target=self.download_picture)
            thread_list.append(thread_save)

        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，该线程不重要。主线程结束，子线程结束
            t.start()

        for q in [self.url_queue, self.html_queue, self.img_queue]:
            q.join()  # 让主线程等待阻塞，等待队列的任务完成之后再完成

        print("主线程结束")


if __name__ == '__main__':
    doutula = DouTuLaSpider()
    doutula.run()
