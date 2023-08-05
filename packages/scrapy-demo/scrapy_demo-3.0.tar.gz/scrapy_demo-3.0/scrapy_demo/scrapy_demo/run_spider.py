# -*- coding: utf-8 -*-
# @Author : zhy
# @Time   : 2022-05-25
# @File   : run_spider.py
import json
from scrapy import cmdline
from scrapy_demo import settings


class Spider(object):
    def __init__(self, file_path):
        self.file_path = file_path

    # pipline
    @staticmethod
    def change_pipline(pipeline_data: dict):
        save_type = pipeline_data.get('type')
        if save_type == 'mongo':
            settings.HOST = pipeline_data.get('host')
            settings.PORT = pipeline_data.get('port')
            settings.DB = pipeline_data.get('db')
            settings.COLLECTION = pipeline_data.get("collection")
            settings.ITEM_PIPELINES = {
                'scrapy_demo.pipelines.SpiderMongoDemoPipeline': 300,
            }
        elif save_type == 'csv':
            settings.FILE_PATH = pipeline_data.get('file_path')
            settings.ITEM_PIPELINES = {
                'scrapy_demo.pipelines.SpiderCsvPipeline': 300,
            }
        elif save_type == 'mysql':
            pass
        else:
            pass

    # setting
    @staticmethod
    def change_setting(json_data: dict):
        settings.DATAS = json_data.get('datas')
        settings.RETRY_TIMES = json_data.get('RETRY_TIMES')
        settings.DOWNLOAD_DELAY = json_data.get('DOWNLOAD_DELAY')
        headers = json_data.get('DEFAULT_REQUEST_HEADERS')
        if headers == None:
            settings.DOWNLOADER_MIDDLEWARES = {
                'scrapy_demo.middlewares.ScrapyDemoDownloaderMiddleware': 543,
            }
        else:
            settings.DEFAULT_REQUEST_HEADERS = json_data.get('DEFAULT_REQUEST_HEADERS')
        settings.ALLOWED_DOMAINS = json_data.get('allowed_domains')
        settings.START_URL = json_data.get('start_url')
        # settings.START_PAGE = json_data.get('start_page')
        # settings.END_PAGE = json_data.get('end_page')

    def run(self):
        json_data = json.load(open(self.file_path, 'r', encoding="utf-8"))
        self.change_pipline(pipeline_data=json_data.get('save_pipeline'))
        self.change_setting(json_data=json_data)
        # 运行爬虫
        cmdline.execute('scrapy crawl test'.split())
        pass


if __name__ == '__main__':
    file_path = r'C:\Users\17580\Desktop\scrapy-redis分享\demo.json'
    spider = Spider(file_path=file_path)
    spider.run()
