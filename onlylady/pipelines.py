# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from onlylady.items import OnlyLadyItem
import requests
import os

class IntoTextPipeline(object):
    def process_item(self, item, spider):
        image_path = os.path.join(os.path.dirname(__file__),"onlylady")
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_url = item['image_url']
        i = len(os.listdir('onlylady')) + 1
        # file_name = image_path + '/' + 'onlylady_' + str(i) + '.jpg'
        try:
            pic = requests.get(image_url,timeout=10)
        except:
            print("无法下载图片！")
        file_name = image_path + '/' + 'onlylady_' + str(i) + '.jpg'
        f = open(file_name,"wb")
        f.write(pic.content)
        f.close()
        image_name = file_name.split('/')[-1]
        a = [item['zh_name'], item['brand'], item['type'], item['price'], image_name]
        result = '@'.join(a)
        with open("onlylady.txt","a") as t:
            t.write(result + "####")
            t.close()

        return item

class WyIntoTextPipeline(object):
    def process_item(self, item, spider):
        image_path = os.path.join(os.path.dirname(__file__),"Wylady")
        if not os.path.exists(image_path):
            os.makedirs(image_path)
        image_url = item['good_image_url']
        i = len(os.listdir('wylady')) + 1
        # file_name = image_path + '/' + 'onlylady_' + str(i) + '.jpg'
        try:
            pic = requests.get(image_url,timeout=10)
        except:
            print("无法下载图片！")
        file_name = image_path + '/' + 'wylady_' + str(i) + '.jpg'
        f = open(file_name,"wb")
        f.write(pic.content)
        f.close()
        image_name = file_name.split('/')[-1]
        a = [item['brand'], item['name'], item['type'], item['detail'] ,item['price'], image_name]
        result = '@'.join(a)
        with open("wylady.txt","a") as t:
            t.write(result + "####")
            t.close()

        return item