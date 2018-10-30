# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from onlylady.settings import UserAgentList
import random

from fake_useragent import UserAgent


from onlylady.tools import proxy

class OnlyladySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class MyUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self,user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        agent = random.choice(list(UserAgentList))
        request.headers['User-Agent'] = agent

class FakeUseragentMiddle(UserAgentMiddleware):

    def __init__(self,user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers['User-Agent'] = ua.random

class ProxyIpMiddleware(object):
    # proxy_list = [
    #     "http://180.76.154.5:8888",
    #     "http://14.109.107.1:8998",
    #     "http://106.46.136.159:808",
    #     "http://175.155.24.107:808",
    #     "http://124.88.67.10:80",
    #     "http://124.88.67.14:80",
    #     "http://58.23.122.79:8118",
    #     "http://123.157.146.116:8123",
    #     "http://124.88.67.21:843",
    #     "http://106.46.136.226:808",
    #     "http://101.81.120.58:8118",
    #     "http://180.175.145.148:808"
    # ]
    proxy_list = proxy.get_ip()

    def process_request(self,request,spider):
        ip = random.choice(self.proxy_list)
        print(ip)
        request.meta['proxy'] = ip