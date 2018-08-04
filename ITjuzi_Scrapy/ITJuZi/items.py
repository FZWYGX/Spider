# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class ItjuziItem(scrapy.Item):
    # 公司名称
    name = scrapy.Field()
    nameFull = scrapy.Field()
    # 公司id
    id = scrapy.Field()
    # 公司url
    url = scrapy.Field()
    # 公司介绍
    profile = scrapy.Field()
    # 公司标签
    slogan = scrapy.Field()
    # 公司的基本信息
    baseInfo = scrapy.Field()
    # 公司的团队信息
    teamInfo = scrapy.Field()
    # 行业分析html代码
    analysis = scrapy.Field()
    # 行业报告
    report = scrapy.Field()
    # 工商信息
    AICInfo = scrapy.Field()

