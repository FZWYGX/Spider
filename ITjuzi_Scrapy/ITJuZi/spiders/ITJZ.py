# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from ..items import ItjuziItem
from scrapy_redis.spiders import RedisCrawlSpider


class ItjzSpider(RedisCrawlSpider):
    name = 'ITJZ'
    allowed_domains = ['www.itjuzi.com']
    # start_urls = ['http://www.itjuzi.com/']
    redis_key = 'ITjuzi:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'/company/\d+'), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/tag/\d+'), follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        item = ItjuziItem()
        # 定义第一个大分类
        demo1 = response.xpath("//div[@class='on-edit-hide']")

        # 公司名称
        name = demo1.xpath("//span[@class='title']/h1//text()").extract()
        item["name"] = [i.strip() for i in name if len(i.strip()) > 0][0]
        item["nameFull"] = demo1.xpath("//span[@class='title']/h1/@data-fullname").extract_first()

        # 公司id
        id = re.findall(r'\d+', response.url)
        item["id"] = id[0]

        # 公司url
        item["url"] = response.url

        # 公司介绍
        profile = demo1.xpath("//div[@class='info-line']//text()").extract()
        item["profile"] = ",".join(i.strip() for i in profile if len(i.strip()) > 0)


        # 公司标签
        slogan = demo1.xpath("//div[@class='rowfoot']//text()").extract()
        slogan = [i.strip() for i in slogan if len(i.strip()) > 0]
        for i in range(len(slogan)):
            if "专辑" in slogan[i]:
                item["slogan"] = slogan[0:i]
                break

        # 定义第二个大分类
        demo2 = response.xpath("//div[@class='main-left-container']")
        # 公司的基本信息
        baseInfo = demo2.xpath("//div[contains(@class, 'block-inc-info')]//text()").extract()
        item["baseInfo"] = [i.strip() for i in baseInfo if len(i.strip()) > 0]
        # 公司的团队信息
        teamInfo = demo2.xpath("//ul[@class='list-unstyled team-list limited-itemnum']//text()").extract()
        item["teamInfo"] = [i.strip() for i in teamInfo if len(i.strip()) > 0][0:-1]
        # 行业分析html代码
        item["analysis"] = demo2.xpath("//div[@id='echart']").extract()
        # 行业报告
        report = demo2.xpath("//ul[@class='list-unstyled analysis-report-list']//li/a/text()").extract()
        report = [i.strip() for i in report if len(i.strip()) > 0]
        report_href = demo2.xpath("//ul[@class='list-unstyled analysis-report-list']//li/a/@href").extract()
        item["report"] = {report[i]: report_href[i] for i in range(len(report))}

        # 工商信息
        AICInfo = demo2.xpath("//div[@id='indus_base']//text()").extract()
        item["AICInfo"] = [i.strip() for i in AICInfo if len(i.strip()) > 0]
        yield item