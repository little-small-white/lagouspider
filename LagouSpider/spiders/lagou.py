# -*- coding: utf-8 -*-
import scrapy
import re
import time
from selenium import webdriver
from urllib import parse
from LagouSpider.items import LagouItem


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    def parse(self, response):
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, x) for x in all_urls if x.startswith('https')]  # 列表生成式
        for url in all_urls:
            re_match = re.match("^https://www.lagou.com/jobs/\d+.html$", url)
            if re_match:
                yield scrapy.Request(url, callback=self.parse_data)
        for url in all_urls:
            re_url = re.match("^https://www.lagou.com/zhaopin/\w+/$", url)
            re_url_2 = re.match("^https://www.lagou.com/zhaopin/\w+/\d+/$", url)
            if re_url or re_url_2:
                yield scrapy.Request(url, callback=self.parse)

    def parse_data(self, response):
        lagou_item = LagouItem()
        re_match = re.match('^https://www.lagou.com/jobs/(\d+).html$', response.url)
        lagou_id = re_match.group(1) if re_match else 0
        lagou_item["Position_name"] = response.css(".job-name span::text").extract_first("")
        lagou_item["wages"] = response.css(".job_request .salary::text").extract_first("")
        lagou_item["job_city"] = response.xpath('//*[@class="job_request"]/p/span[2]/text()').extract_first("").replace("/", "").strip()
        lagou_item["experience"] = response.xpath('//*[@class="job_request"]/p/span[3]/text()').extract_first("").replace("/", "").strip()
        lagou_item["Education"] = response.xpath('//*[@class="job_request"]/p/span[4]/text()').extract_first("").replace("/", "").strip()
        lagou_item["property"] = response.xpath('//*[@class="job_request"]/p/span[5]/text()').extract_first("")
        lagou_item["classification"] = response.css(".position-label li::text").extract()
        lagou_item["create_time"] = response.css(".publish_time::text").extract_first("")
        lagou_item["Advantage"] = response.css(".job-advantage p::text").extract_first("")
        lagou_item["content"] = response.css(".job_bt div").extract_first("")
        lagou_item["address"] = response.css(".work_addr::text").extract()
        lagou_item["company_url"] = response.css(".c_feature a::attr(href)").extract_first("")
        lagou_item["lagou_id"] = lagou_id
        yield lagou_item

    def start_requests(self):
        # 入口处先登录
        # brower = webdriver.Chrome()
        brower = webdriver.Chrome()
        login_url = "https://passport.lagou.com/login/login.html"
        brower.get(login_url)
        brower.find_element_by_css_selector('form.active div[data-propertyname="username"] input').send_keys("1807490****")
        brower.find_element_by_css_selector('form.active div[data-propertyname="password"] input').send_keys("*******")
        brower.find_element_by_css_selector('form.active input.btn_block').click()
        time.sleep(5)
        cookies = brower.get_cookies()
        dict_cookie = {cookie["name"]: cookie["value"] for cookie in cookies}
        brower.close()

        # 添加cookie到Request
        yield scrapy.Request(self.start_urls[0], dont_filter=True, cookies=dict_cookie)