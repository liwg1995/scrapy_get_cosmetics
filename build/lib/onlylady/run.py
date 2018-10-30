# conding:utf8

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "ol"])
execute(['scrapy', 'crawl', 'wylady'])
