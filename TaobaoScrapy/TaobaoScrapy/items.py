# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoscrapyItem(scrapy.Item):

    keyword = scrapy.Field()

    image = scrapy.Field()

    price = scrapy.Field()

    deal = scrapy.Field()

    title = scrapy.Field()

    shop = scrapy.Field()

    location = scrapy.Field()
