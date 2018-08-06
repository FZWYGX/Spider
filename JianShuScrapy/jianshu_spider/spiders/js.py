# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import ArticleItem
import re


class JsSpider(CrawlSpider):
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{11,13}.*'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):

        title = response.xpath("//h1[@class='title']/text()").extract_first()
        author_picture = response.xpath("//a[@class='avatar']/img/@src").extract_first()
        author = response.xpath("//span[@class='name']/a/text()").extract_first()
        pub_time = response.xpath("//span[@class='publish-time']/text()").extract_first()
        url = response.url
        url_spilt = url.split("?")[0]
        article_id = url_spilt.split("/")[-1]

        content = response.xpath("//div[@class='show-content']").extract_first()

        word_count = re.findall(r'\"public_wordage\":(.*?),', response.body.decode())

        comment_count = re.findall(r'\"comments_count\":(.*?),', response.body.decode())
        read_count = re.findall(r'\"views_count\":0:(.*?),', response.body.decode())
        like_count = re.findall(r'\"likes_count\":(.*?),', response.body.decode())

        item = ArticleItem(
            title=title,
            author_picture=author_picture,
            author=author,
            article_id=article_id,
            article_url=response.url,
            pub_time=pub_time,
            word_count=word_count,
            read_count=read_count,
            comment_count=comment_count,
            like_count=like_count,
            content=content,
        )
        print(item)
        yield item
