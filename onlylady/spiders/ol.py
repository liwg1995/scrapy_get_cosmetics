# -*- coding: utf-8 -*-
import scrapy

from onlylady.items import OnlyLadyItem


class OlSpider(scrapy.Spider):
    name = 'ol'  # 爬虫名称
    allowed_domains = ['hzp.onlylady.com']  # 允许这个爬虫爬取的域名
    start_urls = ['http://hzp.onlylady.com/brand.html']  # 起始的页面
    headers = {
        "HOST": "hzp.onlylady.com",
        "Referer": "http://hzp.onlylady.com/cosmetics.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
    }

    # 设置headers，下面的每一个如果要接着爬取的时候，写进入

    def parse(self, response):
        # 获取所有品牌的链接
        brand_urls = response.css('#sortByLetter .brandsWraper a::attr(href)').extract()
        for brand_url in set(brand_urls):
            yield scrapy.Request(brand_url, headers=self.headers, callback=self.more)

    def more(self, response):
        # 进入某个品牌链接之后，获取进入所有商品的链接
        more_url = response.css('.more::attr(href)').extract_first('')
        yield scrapy.Request(more_url, headers=self.headers, callback=self.goods)

    def goods(self, response):
        # 进入所有商品的链接之后，获取商品的详情链接，以及图片链接
        goods_nodes = response.css('.commentItem .left .imgWraper a')
        for goods_node in goods_nodes:
            goods_url = goods_node.css('::attr(href)').extract_first('')  # 获取商品详情页链接
            image_url = goods_node.css('img::attr(src)').extract_first('')  # 获取商品展示图片的连接
            yield scrapy.Request(goods_url, headers=self.headers, meta={"image_url": image_url}, callback=self.detail)
            # meta表示把图片的url暂时存起来，下面的一些函数可以来meta来接收这个参数

        # 获取下一页的信息，处理分页的逻辑
        next_url = response.css('.comment_bar .page .next::attr(href)').extract_first('')
        if next_url:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.goods)

    def detail(self, response):
        # 到达详情页之后，获取详情页中的一些参数，并提交到我们编写的OnlyLadyItem()中，yield提交items
        zh_name = response.css('.detail_pro .detail_l .p_r .name h2::text').extract_first('')
        type = response.css('.detail_pro .detail_l .p_r dl')[0].css('dd a::attr(title)')[0].extract()
        brand = \
            response.css('.detail_pro .detail_l .p_r dl')[0].css('dd')[1].css('a::attr(title)').extract_first('').split(
                ' ')[0]
        try:
            price = response.css('.price::text').extract_first('').split('￥')[-1]
        except:
            price = ""
        image_url = response.meta.get('image_url', 'image_url')  # 通过response.meta.get来接收上个函数存储的meta中的image_url
        items = OnlyLadyItem()
        items['zh_name'] = zh_name
        items['type'] = type
        items['brand'] = brand
        items['price'] = price
        items['image_url'] = image_url
        yield items
