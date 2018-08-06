# -*- coding:utf-8 -*-
import requests
import json
from lxml import etree
import time
import csv


class LaGouSpider(object):
    def __init__(self):
        self.headers = {
            'Cookie': 'JSESSIONID=ABAAABAAAGGABCBA3FD7A4F9DA79F9F721F243606315918; _ga=GA1.2.567488664.1532995624; _gid=GA1.2.352401045.1532995624; _gat=1; user_trace_token=20180731080931-ff4484c6-9455-11e8-a085-5254005c3644; LGSID=20180731080931-ff4486b5-9455-11e8-a085-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGUID=20180731080931-ff448865-9455-11e8-a085-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532995625; index_location_city=%E6%88%90%E9%83%BD; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532995627; LGRID=20180731080934-011840e9-9456-11e8-abf7-525400f775ce',
            'Host': 'www.lagou.com',
            'Upgrade-Insecure-Requests': "1",
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

        self.post_data = {
            'first': 'true',
            'pn': '',
            'kd': '',
        }
        self.base_url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'

        with open("拉钩职位.csv", "a", encoding="utf-8") as f:
            f.write("公司全称,公司简称,职位,工作年限,教育程度,薪资,所在城市,公司规模,职位描述,工作地址,拉钩公司网址和公司源网址" + "\n")

    def parse_url_post(self, url, data):
        try:
            response = requests.post(url, headers=self.headers, data=data)
            return response.text
        except:
            return None

    def get_content_list(self, json_res):
        dict_res = json.loads(json_res)
        result_list = dict_res["content"]["positionResult"]["result"]

        list_dict = []
        for result in result_list:
            dict = {}
            dict["FullName"] = result["companyFullName"]  # 公司全称
            dict["ShortName"] = result["companyShortName"]  # 公司简称
            dict["jobName"] = result["positionName"]  # 职位
            dict["workYear"] = result["workYear"]  # 工作年限
            dict["education"] = result["education"]  # 教育程度
            dict["salary"] = result["salary"]  # 薪资
            dict["city"] = result["city"]  # 所在城市
            dict["companySize"] = result["companySize"]  # 公司规模
            dict["welfare"] = result["companyLabelList"]  # 公司福利
            detail_url = ("https://www.lagou.com/jobs/"+str(result["positionId"])+".html" ) if len(str(result["positionId"])) > 0 else None
            try:
                html = requests.get(detail_url, headers=self.headers).text
                html = etree.HTML(html)
                description = html.xpath("//dl[@id='job_detail']/dd[@class='job_bt']//text()")
                dict["description"] = [i.strip() for i in description if len(i.strip()) > 0]  # 职位描述
                address = html.xpath("//dl[@id='job_detail']/dd[@class='job-address clearfix']//text()")
                dict["address"] = "".join(i.strip() for i in address if len(i.strip()) > 0)  # 工作地址
                dict["href"] = html.xpath("//dl[@id='job_company']//a/@href")  # 拉钩公司网址和公司源网址
            except:
                dict["description"] = ""
                dict["address"] = ""
                dict["href"] = ""
            list_dict.append(dict)
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
                description = dict["description"]
                address = dict["address"]
                href = dict["href"]
                data = [(FullName, ShortName, jobName, workYear, education, salary,
                         city, companySize, welfare, description, address, href)]
                writer.writerows(data)
        f.close()

    def run(self):
        city_list = ["上海", "成都"]
        job_list = ["爬虫", "数据分析", "人工智能"]
        for city in city_list:
            print("正在爬取城市: {}".format(city))
            url = self.base_url.format(city)
            for i in range(1, 5):
                self.post_data["pn"] = i
                for job in job_list:
                    self.post_data["kd"] = job
                    print(self.post_data)
                    json_res = self.parse_url_post(url, self.post_data)
                    if json_res is not None:
                        list_dict = self.get_content_list(json_res)
                        self.save_content_list(list_dict)
                        time.sleep(10)


if __name__ == '__main__':
    lagou = LaGouSpider()
    lagou.run()
