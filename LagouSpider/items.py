# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    Position_name = scrapy.Field()
    wages = scrapy.Field()
    job_city = scrapy.Field()
    experience = scrapy.Field()
    Education = scrapy.Field()
    property = scrapy.Field()
    classification = scrapy.Field()
    create_time = scrapy.Field()
    Advantage = scrapy.Field()
    content = scrapy.Field()
    address = scrapy.Field()
    company_url = scrapy.Field()
    lagou_id = scrapy.Field()


    def sql_insert_get(self):
        insert_sql = """
            insert into lagou(
                                Position_name, wages, job_city,
                                experience, Education, property,
                                classification, create_time, Advantage,
                                content, company_url, lagou_id
                                )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE create_time=VALUES(create_time), content=VALUES(content)
        """

        classification = ".".join(self["classification"])
        lagou_id = int(self["lagou_id"])
        sql_data = (
            self["Position_name"], self["wages"], self["job_city"],
            self["experience"], self["Education"], self["property"],
            classification, self["create_time"], self["Advantage"],
            self["content"], self["company_url"], lagou_id,
        )

        return insert_sql, sql_data