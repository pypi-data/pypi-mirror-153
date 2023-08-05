# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exporters import CsvItemExporter


class ScrapyDemoPipeline:
    def process_item(self, item, spider):
        return item


class SpiderMongoDemoPipeline:
    def open_spider(self, spider):
        from .settings import HOST, PORT, DB, COLLECTION
        self.mongo_client = pymongo.MongoClient(HOST, PORT)
        self.db = self.mongo_client[DB]
        self.sheet = self.db[COLLECTION]

    def process_item(self, item, spider):
        print('Pipline:', item)
        self.sheet.insert_one(dict(item))
        return item

    def close_spider(self, spider):
        self.mongo_client.close()


class SpiderCsvPipeline(object):
    def open_spider(self, spider):
        from .settings import FILE_PATH
        # 创建csv格式的文件
        self.file = open(FILE_PATH, "wb+")
        # 创建csv文件读写对象，将数据写入到指定的文件中
        self.csv_exporter = CsvItemExporter(self.file)
        # 开始执行item数据读写
        self.csv_exporter.start_exporting()

    def process_item(self, item, spider):
        print("CSV:", item)
        # 将item数据写入到文件中
        self.csv_exporter.export_item(item)
        return item

    def close_spider(self, spider):
        # 结束文件读写操作
        self.csv_exporter.finish_exporting()
        # 关闭文件
        self.file.close()

class SpiderMySQLPipeline:
    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        print("MySQL:", item)
        pass

    def close_spider(self, spider):
        pass