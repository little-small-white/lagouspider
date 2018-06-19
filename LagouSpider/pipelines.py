# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from MySQLdb.cursors import DictCursor
import MySQLdb
from twisted.enterprise import adbapi


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbprams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            port=3306,
            cursorclass=DictCursor,
            charset='utf8',
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbprams)

        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_sql, item, spider)
        query.addErrback(self.insert_error, item, spider)
        return item

    def insert_sql(self, cursor, item, spider):
        sql_code, item_data = item.sql_insert_get()
        cursor.execute(sql_code, item_data)

    def insert_error(self, failure, item, spider):
        print(failure)
