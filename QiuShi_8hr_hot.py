# coding=utf-8
import requests
from lxml import etree
import threading
from queue import Queue
import json


class QiubaiSpider:
    def __init__(self):
        self.remen_url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        self.hot_url_temp = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
        self.url_queue = Queue()  # 实例化需要请求的url队列
        self.html_queue = Queue()  # 实例化需要解析的html队列
        self.content_queue = Queue()  # 实例化需要存储内容的队列

    def get_url_list(self):
        """
        构造需要请求的url, 并存进url队列中
        """
        for i in range(1, 14):
            self.url_queue.put(self.remen_url_temp.format(i))
        for i in range(1, 14):
            self.url_queue.put(self.hot_url_temp.format(i))

    def parse_url(self):
        """
        发送请求，获取html文本，并存入html队列
        """
        while True:
            # if self.url_queue.empty():
            #     break
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers=self.headers)
            # return response.content.decode()
            self.html_queue.put(response.content.decode())
            self.url_queue.task_done()

    def get_content_list(self):
        """
        从html队列中取出html进行解析, 将解析后的内容存入存储队列中
        """
        while True:
            # if self.url_queue.empty() and self.html_queue.empty():
            #     break
            html_str = self.html_queue.get()
            html = etree.HTML(html_str)
            div_list = html.xpath("//div[@id='content-left']/div")
            content_list = []
            for div in div_list:
                item = {}
                item["content"] = div.xpath(".//div[@class='content']/span/text()")
                item["content"] = [i.replace("\n", "") for i in item["content"]]
                item["author_gender"] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
                item["author_gender"] = item["author_gender"][0].split(" ")[-1].replace("Icon", "") if len(item["author_gender"]) > 0 else None
                item["author_age"] = div.xpath(".//div[contains(@class,'articleGender')]/text()")
                item["author_age"] = item["author_age"][0] if len(item["author_age"]) > 0 else None
                item["content_img"] = div.xpath(".//div[@class='thumb']/a/img/@src")
                item["content_img"] = "https:" + item["content_img"][0] if len(item["content_img"]) > 0 else None
                item["author_img"] = div.xpath(".//div[@class='author clearfix']//img/@src")
                item["author_img"] = "https:" + item["author_img"][0] if len(item["author_img"]) > 0 else None
                item["stats_vote"] = div.xpath(".//span[@class='stats-vote']/i/text()")
                item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"]) > 0 else None
                item["stats-comments"] = div.xpath(".//span[@class='stats-comments-vote']/i/text()")
                item["stats-comments"] = item["stats-comments"][0] if len(item["stats-comments"]) > 0 else None
                content_list.append(item)
            self.content_queue.put(content_list)
            self.html_queue.task_done()

    def save_content_list(self):
        """
        存储内容
        """
        while True:
            # if self.html_queue.empty() and self.content_queue.empty():
            #     break
            content_list = self.content_queue.get()
            with open('糗事百科2.txt', 'a', encoding='utf-8') as f:
                for content in content_list:
                    f.write(json.dumps(content, ensure_ascii=False))
                    f.write("\n")
                    print(content)
            self.content_queue.task_done()

    def run(self):  # 实现主要逻辑
        thread_list = []

        # 1.url_list
        thread_url = threading.Thread(target=self.get_url_list)
        thread_list.append(thread_url)

        # 2.遍历，发送请求，获取响应
        for i in range(10):
            thread_parse = threading.Thread(target=self.parse_url)
            thread_list.append(thread_parse)

        # 3.提取数据
        for i in range(4):
            thread_html = threading.Thread(target=self.get_content_list)
            thread_list.append(thread_html)

        # 4.保存
        thread_save = threading.Thread(target=self.save_content_list)
        thread_list.append(thread_save)

        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，该线程不重要。主线程结束，子线程结束
            t.start()

        for q in [self.url_queue, self.html_queue, self.content_queue]:
            q.join()  # 让主线程等待阻塞，等待队列的任务完成之后再完成

        print("主线程结束")


if __name__ == '__main__':
    qiubai = QiubaiSpider()
    qiubai.run()



