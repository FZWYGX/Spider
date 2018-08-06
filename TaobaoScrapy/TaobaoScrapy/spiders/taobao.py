# -*- coding: utf-8 -*-
from scrapy.http import Request
from pyquery import PyQuery as py
from urllib import parse
from ..items import *


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']

    def start_requests(self):
        keywords = ['女装', '男装', '美妆', '洗护', '保健品', '珠宝', '眼镜', '手表', '运动', '户外', '乐器', '游戏', '动漫', '影视', '美食', '生鲜',
                    '零食', '鲜花', '宠物', '农资', '房产', '装修', '建材', '家具', '家饰', '家纺', '汽车', '二手车', '办公', 'DIY', '五金电子', '百货',
                    '餐厨', '家庭保健', '学习', '卡券', '本地服务']
        for keyword in keywords:
            for page in range(1, self.settings.get('MAX_PAGE') + 1):
                url = 'https://s.taobao.com/search?q=' + parse.quote(keyword)
                yield Request(url=url,
                              callback=self.parse_detail,
                              meta={'page': page, 'keyword': keyword},
                              dont_filter=True)

    def parse_detail(self, response):
        doc = py(response.text)
        products = doc(
            '#mainsrp-itemlist .items .item').items()
        for product in products:
            item = TaobaoscrapyItem()
            item['price'] = product.find('.price').text()
            item['title'] = product.find('.title').text()
            item['shop'] = product.find('.shop').text()
            item['image'] = product.find('.pic .img').attr('src')
            item['deal'] = product.find('.deal-cnt').text()
            item['location'] = product.find('.location').text()
            item['keyword'] = response.meta['keyword']
            yield item
