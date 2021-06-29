# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from .items import Xm1Item

class Xm1Pipeline:
    def open_spider(self,spider):
        config = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '',
            'db': 'xu_nian_sha',  # 数据库中库的名字
            'charset': 'utf8'}
        self.conn = pymysql.connect(**config)
        self.cursor = self.conn.cursor()
        spider.conn = self.conn
        spider.cursor = self.cursor
    #
    def process_item(self, item, spider):
        if isinstance(item, Xm1Item):  # 减少bug产生，item文件
            sql = "insert  into  xns(title,digests,times,two_url) values(%s,%s,%s,%s)"
            self.cursor.execute(sql, (
                item['title'],
                item['digests'],
                item['time'],
                item['picture'],
                item['content'],
                item['two_url'],
            ))
            self.conn.commit()  # 提交
            return item
    #
    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

