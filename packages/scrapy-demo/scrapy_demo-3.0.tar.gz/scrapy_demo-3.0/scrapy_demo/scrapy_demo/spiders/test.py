from copy import deepcopy

import scrapy

from scrapy_demo import settings
from scrapy import Item, Field



def xpath_item(item, datas, response):
    for data in datas:
        if '/' in data:
            ul_li = response.xpath(data)
            for ul in ul_li:
                xpath_item(item, datas[data], ul)
        else:
            item.fields[data] = Field()
            item[data] = response.xpath(datas[data]).extract_first()
    return item


class BaiduSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = settings.ALLOWED_DOMAINS
    start_urls = settings.START_URL

    def parse(self, response):
        item = Item()
        datas = settings.DATAS
        for data in datas:
            if '/' in data:
                ul_li = response.xpath(data)
                for ul in ul_li:
                    xpath_item(item, datas[data], ul)
                    yield item
            else:
                item.fields[data] = Field()
                item[data] = response.xpath(datas[data]).extract_first()

