# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class OnlyLadyItem(scrapy.Item):
    zh_name = scrapy.Field()
    type = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    image_url = scrapy.Field()


class WyladyItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    detail = scrapy.Field()
    price = scrapy.Field()
    good_image_url = scrapy.Field()
