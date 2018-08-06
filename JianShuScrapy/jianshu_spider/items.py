# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()  # 标题
    author_picture = scrapy.Field()  # 作者图片地址
    author = scrapy.Field()  # 作者
    article_id = scrapy.Field()  # 作者id
    article_url = scrapy.Field()  # 文章url
    pub_time = scrapy.Field()  # 发布日期
    word_count = scrapy.Field()  # 字数
    read_count = scrapy.Field()  # 阅读数量
    comment_count = scrapy.Field()  # 评论数量
    like_count = scrapy.Field()  # 喜欢数
    content = scrapy.Field()  # 文章内容




