import scrapy
import random
import time
import re
import logging
from scrapy.crawler import CrawlerProcess

# local imports
import stock_names


class StockSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/S/.DJI',          # 道琼斯指数
                  'https://xueqiu.com/S/.IXIC',         # 纳斯达克综合指数
                  'https://xueqiu.com/S/.INX',          # 标普500指数
                  'https://xueqiu.com/S/SH000688',      # 科创50
                  'https://xueqiu.com/S/SH000016',      # 上证50
                  'https://xueqiu.com/S/SH000300',      # 沪深300
                  'https://xueqiu.com/S/BJ899050',      # 北证50
                  'https://xueqiu.com/S/HKHSI',         # 恒生指数
                  'https://xueqiu.com/S/HKHSTECH',      # 恒生科创指数
                  'https://xueqiu.com/S/HKHSCEI'        # 国企指数
                  ]
    custom_settings = {
        # Ignore some warnings and logs
        'LOG_LEVEL': logging.CRITICAL,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7'
    }

    stock_data=[]
    def start_requests(self):
        # TODO: 做一个动态的请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://xueqiu.com/S/.DJI'
        }
        print("-----Current Stock Market Indexes-----")
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        # Xpaths
        quote_container = response.xpath("//div[@class='quote-container']//div[@class='stock-info']")
        # Xueqiu regard rising & falling as different
        stock_rise = quote_container.xpath(".//div[@class='stock-price stock-rise']//div[@class='stock-current']")
        stock_fall = quote_container.xpath(".//div[@class='stock-price stock-fall']//div[@class='stock-current']")
        # stock change
        stock_change = quote_container.xpath(".//div[@class='stock-change']/text()").get()
        # market status
        market_status = response.xpath("//div[@class='quote-market-status']/span/text()").get()

        # Time
        cur_time = time.time()
        time_str = time.ctime(cur_time)

        # Default extract rise, if none then extract fall
        cur_price = stock_rise.xpath(".//strong/text()").get()
        txt_color = '\033[31m'
        if cur_price is None:
            cur_price = stock_fall.xpath(".//strong/text()").get()
            txt_color = '\033[32m'

        # Protection
        cur_price = 'Unavailable' if cur_price is None else cur_price
        market_status = '' if market_status is None else market_status
        txt_color = '\033[0m' if cur_price is None else txt_color
        stock_change = "Unavailable" if stock_change is None else stock_change

        # Resolve Stock Code
        pattern = r'\/\.?([A-Z0-9]+)$'
        match = re.search(pattern, response.url)
        if match:
            stock_code = match.group(1)
        else:
            stock_code = "Unknown"

        # Stock Name
        stock_name = stock_names.stock[stock_code]

        self.stock_data.append(
            {
                "Stock Code": stock_code,
                "Stock Name CN": stock_name,
                "Current Price": cur_price,
                "Stock Change": stock_change,
                "Current Time": time_str
            }
        )
        print(
            txt_color +
            stock_name+'('+stock_code + ')' + '(' + market_status + ')\n'
            'Current Price: ' + cur_price + '\n' +
            'Stock Change: ' + stock_change
            )
        print('Current Time: '+time_str)
        print('\n')


def run_spider():
    # 创建CrawlerProcess实例
    process = CrawlerProcess()
    # 添加爬虫到CrawlerProcess实例
    process.crawl(StockSpider)
    # 启动爬虫
    process.start()

# Run this spider
run_spider()
