from email import header
from email.policy import default
from requests import request
from scrapy.selector import Selector
import scrapy
from dangdang.items import DangdangItem
import logging
import time

class DangdangbookSpider(scrapy.Spider):
    name = 'dangdangbook'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://bang.dangdang.com/books/bestsellers/']
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    def start_requests(self):
        for offset in range(2,3):
            url = [i + f'01.00.00.00.00.00-24hours-0-0-1-{offset}'for i in self.start_urls][0]
            logging.info('scrapying %s',url)
            yield scrapy.Request(url,headers = self.header,callback= self.parse)

    # def parse(self,response):
    #     item = DangdangItem()
    #     for name in response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "name", " " ))]//a/text()'):
    #         item['name'] = name
    #         print(item['name'])
    #     return item
    def parse(self, response):
        logging.info('begin scrapying href')
        href_list = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "name", " " ))]//a/@href').getall()
        for href in href_list:
            # time.sleep(3)
            logging.info('scrapying %s',href)

            yield scrapy.Request(url=href,headers=self.header,callback = self.parse_detail)


    def parse_detail(self,response):
        logging.info('scrapying name')
        item = DangdangItem()
        time.sleep(2)
        item['name'] = response.xpath('//h1/@title').get()
        item['author'] = response.xpath('//*[(@id = "author")]//a/text()').getall()
        item['publish'] = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "t1", " " )) and (((count(preceding-sibling::*) + 1) = 2) and parent::*)]//a/text()').get()
        item['publish_time'] = response.css('.t1:nth-child(3)::text').get()
        print(item['name'],item['author'],item['publish'],item['publish_time'])
        return item

    # def parse_index(self,response):
    #     logging.info('jump ok')
    #     for item in response.css('.li'):
    #         href = item.xpath('//@class="name"/a/@href').extract_first()
    #         logging.info('jump %s',href)
    #         yield scrapy.request(url = href ,callback = self.parse_response,headers = self.header)    


    # def parse_response(self,response):
    #     sel = Selector(response)
    #     tree = etree.HTML(sel)
    #     item = DangdangItem()
    #     name = tree.css('div.name_info').xpath('h1/@title').extract_first()
    #     authors = tree.css('span.author').xpath('a/text()').extract()
    #     publisher = tree.css('span.publisher_info').xpath('a/text()').extract_first()
    #     publish_time = tree.css('div.publisher_info').xpath('span/text()').extract_first()
    #     classify = tree.css('a.__Breadcrumb_pub::text()').extract()
    #     author = [author.strip() for author in authors] if authors else []
    #     item = DangdangItem(name=name, authors=authors, publisher=publisher,
    #                     publish_time=publish_time, classify=classify,author=author)
    #     return item


