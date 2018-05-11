# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from onlylady.items import WyladyItem


class WyladySpider(scrapy.Spider):
    name = 'wylady'
    allowed_domains = ['cosmetic.lady.163.com']
    start_urls = ['http://cosmetic.lady.163.com/search/product/']
    headers = {
        "Host": "cosmetic.lady.163.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

    def parse(self, response):
        goods_urls = response.css('#listTop .ph-20 .mod-dataBox .dataBox-side h3 a::attr(href)').extract()
        goods_image_urls = response.css('#listTop .ph-20 .mod-dataBox .dataBox-side a img::attr(src)').extract()
        for goods_url in goods_urls:
            good_url = parse.urljoin(response.url, goods_url)
        for good_image_url in goods_image_urls:
            if good_image_url != 'http://img1.cache.netease.com/pcluster/cosmetic/product/f12/da9/37e/18edb99aa539f64c865da20_100x100.png':
                yield scrapy.Request(url=good_url, headers=self.headers, meta={"good_image_url": good_image_url},
                                     callback=self.details)
            else:
                continue
                
        next_urls = response.css('.pages a::attr(href)')[-2].extract()
        next_url = parse.urljoin(response.url, next_urls)
        yield scrapy.Request(url=next_url, headers=self.headers, callback=self.parse)

    def details(self, response):
        brand = response.css('.detailbox-main h1 a::text').extract_first('')
        name = response.css('.detailbox-main h1::text').extract_first('').split('-')[-1]
        type = response.css('.infolist2 li')[1].css('a::text')[1].extract()
        detail = response.css('#descLong::text').extract_first('').replace(' \r', '')
        price = response.css('.infolist2 li')[2].css('::text')[-1].extract().split('/')[0].replace('元', '')
        good_image_url = response.meta.get('good_image_url')
        items = WyladyItem()
        items['brand'] = brand
        items['name'] = name
        items['type'] = type
        items['detail'] = detail
        items['price'] = price
        items['good_image_url'] = good_image_url
        yield items
