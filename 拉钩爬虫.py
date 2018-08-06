# -*- coding:utf-8 -*-
import requests
import json
from lxml import etree
from urllib import parse
import time
import csv


class LaGouSpider(object):
    def __init__(self):
        self.headers = {
            'Cookie': 'JSESSIONID=ABAAABAAAFCAAEGE5369BF622EF733FA62C1159B199B07D; user_trace_token=20180806143340-3015e84e-63f5-450e-a0a1-43c94e98a8fd; _ga=GA1.2.472866035.1533537058; _gat=1; LGSID=20180806143341-a8ba6de7-9942-11e8-a341-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F4846942.html; LGRID=20180806143341-a8ba6f6a-9942-11e8-a341-5254005c3644; LGUID=20180806143341-a8ba6fca-9942-11e8-a341-5254005c3644; _gid=GA1.2.1146742746.1533537058; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533537058; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1533537058',
            # 预留位子, 等待代码部分实现替换
            'Referer': None,
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

        self.post_data = {
            'first': 'true',
            # 预留位子, 等待代码部分实现替换
            'pn': None,
            # 预留位子, 等待代码部分实现替换
            'kd': None,
        }
        # 拉钩职位json数据的url
        self.base_url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'

        # 直接存储为csv文件
        with open("拉钩职位.csv", "a", encoding="utf-8") as f:
            f.write("公司全称,公司简称,职位,工作年限,教育程度,薪资,所在城市,公司规模,职位描述,工作地址,拉钩公司网址和公司源网址" + "\n")

    def parse_url_post(self, url, data):
        try:
            # 发送请求
            response = requests.post(url, headers=self.headers, data=data)
            return response.text
        except:
            return None

    def get_content_list(self, json_res):
        # json.loads:  json字符串 --> python数据类型
        dict_res = json.loads(json_res)
        result_list = dict_res["content"]["positionResult"]["result"]

        list_dict = []
        for result in result_list:
            dict = {}
            # 公司全称
            dict["FullName"] = result["companyFullName"]
            # 公司简称
            dict["ShortName"] = result["companyShortName"]
            # 职位
            dict["jobName"] = result["positionName"]
            # 工作年限
            dict["workYear"] = result["workYear"]
            # 教育程度
            dict["education"] = result["education"]
            # 薪资
            dict["salary"] = result["salary"]
            # 所在城市
            dict["city"] = result["city"]
            # 公司规模
            dict["companySize"] = result["companySize"]
            # 公司福利
            dict["welfare"] = result["companyLabelList"]
            # 是否有详情页, 如果有, 进入详情页抓取
            detail_url = ("https://www.lagou.com/jobs/"+str(result["positionId"])+".html" ) if len(str(result["positionId"])) > 0 else None
            try:
                html = requests.get(detail_url, headers=self.headers).text
                html = etree.HTML(html)
                description = html.xpath("//dl[@id='job_detail']/dd[@class='job_bt']//text()")
                # 职位描述
                dict["description"] = [i.strip() for i in description if len(i.strip()) > 0]

                # 工作地址
                address = html.xpath("//dl[@id='job_detail']/dd[@class='job-address clearfix']//text()")
                dict["address"] = "".join(i.strip() for i in address if len(i.strip()) > 0)

                # 拉钩公司网址和公司源网址
                dict["href"] = html.xpath("//dl[@id='job_company']//a/@href")
            except:
                dict["description"] = ""
                dict["address"] = ""
                dict["href"] = ""
            list_dict.append(dict)
            print(dict)
        return list_dict

    def save_content_list(self, list_dict):

        with open('拉钩职位.csv', 'a', encoding="utf-8") as f:
            writer = csv.writer(f)
            for dict in list_dict:
                FullName = dict["FullName"]  # 公司全称
                ShortName = dict["ShortName"]  # 公司简称
                jobName = dict["jobName"]  # 职位
                workYear = dict["workYear"]  # 工作年限
                education = dict["education"]  # 教育程度
                salary = dict["salary"]  # 薪资
                city = dict["city"]  # 所在城市
                companySize = dict["companySize"]  # 公司规模
                welfare = dict["welfare"]  # 公司福利
                description = dict["description"]  # 职位描述
                address = dict["address"]  # 工作地址
                href = dict["href"]  # 拉钩公司网址和公司源网址
                data = [(FullName, ShortName, jobName, workYear, education, salary,
                         city, companySize, welfare, description, address, href)]
                writer.writerows(data)
        f.close()

    def run(self):
        city_list = ["成都", "上海"]
        job_list = ["爬虫", "数据分析", "人工智能"]
        for city in city_list:
            print("正在爬取城市: {}".format(city))
            url = self.base_url.format(city)
            for i in range(1, 5):
                self.post_data["pn"] = i
                for job in job_list:
                    self.headers["Referer"] = 'https://www.lagou.com/jobs/list_' + parse.quote(job)
                    self.post_data["kd"] = job
                    print(self.post_data)
                    json_res = self.parse_url_post(url, self.post_data)
                    if json_res is not None:
                        list_dict = self.get_content_list(json_res)
                        self.save_content_list(list_dict)
                        time.sleep(3)


if __name__ == '__main__':
    lagou = LaGouSpider()
    lagou.run()
