# -*- coding: utf-8 -*-
import scrapy

from onlylady.items import OnlyLadyItem


class OlSpider(scrapy.Spider):
    name = 'ol'
    allowed_domains = ['hzp.onlylady.com']
    start_urls = ['http://hzp.onlylady.com/brand.html']
    headers = {
        "HOST": "hzp.onlylady.com",
        "Referer": "http://hzp.onlylady.com/cosmetics.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

    def parse(self, response):
        brand_urls = response.css('#sortByLetter .brandsWraper a::attr(href)').extract()
        for brand_url in set(brand_urls):
            yield scrapy.Request(brand_url, headers=self.headers, callback=self.more)

    def more(self, response):
        more_url = response.css('.more::attr(href)').extract_first('')
        yield scrapy.Request(more_url, headers=self.headers, callback=self.goods)

    def goods(self, response):
        goods_nodes = response.css('.commentItem .left .imgWraper a')
        for goods_node in goods_nodes:
            goods_url = goods_node.css('::attr(href)').extract_first('')
            image_url = goods_node.css('img::attr(src)').extract_first('')
            yield scrapy.Request(goods_url, headers=self.headers, meta={"image_url":image_url}, callback=self.detail)

        next_url = response.css('.comment_bar .page .next::attr(href)').extract_first('')
        if next_url:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.goods)

    def detail(self, response):
        zh_name = response.css('.detail_pro .detail_l .p_r .name h2::text').extract_first('')
        type = response.css('.detail_pro .detail_l .p_r dl')[0].css('dd a::attr(title)')[0].extract()
        brand = \
        response.css('.detail_pro .detail_l .p_r dl')[0].css('dd')[1].css('a::attr(title)').extract_first('').split(
            ' ')[0]
        try:
            price = response.css('.price::text').extract_first('').split('￥')[-1]
        except:
            price = ""
        image_url = response.meta.get('image_url','image_url')
        items = OnlyLadyItem()
        items['zh_name'] = zh_name
        items['type'] = type
        items['brand'] = brand
        items['price'] = price
        items['image_url'] = image_url
        yield items