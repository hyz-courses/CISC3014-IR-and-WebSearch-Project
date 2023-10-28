import scrapy
import time
import re
import logging
from scrapy.crawler import CrawlerProcess

class StockRank(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/hq#exchange=US&order=desc&order_by=volume']
    custom_settings = {
        # Ignore some warnings and logs
        'LOG_LEVEL': logging.CRITICAL,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    }

    def start_requests(self):
        # TODO: 做一个动态的请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://xueqiu.com/hq#exchange=US&order=desc&order_by=volume'
        }

        # Crawl all the urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)


    def parse(self, response):
        # All the US stocks
        stock_table = response.xpath("//table[@class='portfolio']/tbody")

        # Stocks
        stock_array = stock_table.xpath("./tr").get()
        print(stock_table)




def run_spider():
    # 创建CrawlerProcess实例
    process = CrawlerProcess()
    # 添加爬虫到CrawlerProcess实例
    process.crawl(StockRank)
    # 启动爬虫
    process.start()


# Run this spider
run_spider()