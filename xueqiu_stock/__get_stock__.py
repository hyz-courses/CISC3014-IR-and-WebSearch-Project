import scrapy
import time
import re
import logging
import pandas as pd
from scrapy.crawler import CrawlerProcess

# local imports
import __stock_terms__
import __quote_info__
import __settings__


class StockSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    is_terminal_beautiful = True
    start_urls = __settings__.urls
    custom_settings = {
        # Terminal settings: Ignore some warnings and logs
        'LOG_LEVEL': logging.CRITICAL if is_terminal_beautiful is True else logging.ERROR,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',

        # Local settings
        'LANG': 'EN',
        'USE_EXACT_VALUES': True,
        'SAVE_DATA': True,
    }

    stock_data = []
    index = 0

    def start_requests(self):
        # TODO: 做一个动态的请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://xueqiu.com/S/.DJI'
        }

        print("\n~~-----Current Stock Market Indexes-----~~\n")

        # Crawl all the urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)


    def parse(self, response):
        # --------- Get required data ---------
        quote_container = response.xpath("//div[@class='quote-container']")
        stock_info = quote_container.xpath(".//div[@class='stock-info']")
        quote_info = quote_container.xpath(".//table[@class='quote-info']//td")        # Quote Info
        # Stock Price
        stock_rise = stock_info.xpath(".//div[@class='stock-price stock-rise']//div[@class='stock-current']")
        stock_fall = stock_info.xpath(".//div[@class='stock-price stock-fall']//div[@class='stock-current']")
        # Stock attributes
        stock_change = stock_info.xpath(".//div[@class='stock-change']/text()").get()                    # stock change
        market_status = response.xpath("//div[@class='quote-market-status']/span/text()").get()          # Market status

        # --------------- Time ----------------
        cur_time = time.time()
        time_str = time.ctime(cur_time)

        # ------------ Stock Price ------------
        # Default extract rise, if none then extract fall
        cur_price = stock_rise.xpath(".//strong/text()").get()
        txt_color = '\033[31m'
        if cur_price is None:
            cur_price = stock_fall.xpath(".//strong/text()").get()
            txt_color = '\033[32m'

        # ---------- Market Status -----------
        if self.custom_settings["LANG"] == "EN" and market_status in __stock_terms__.terms:
            market_status = __stock_terms__.terms[market_status]

        # ------------ Protection ------------
        cur_price = 'Unavailable' if cur_price is None else cur_price
        market_status = '' if market_status is None else market_status
        txt_color = '\033[0m' if cur_price is None else txt_color
        stock_change = "Unavailable" if stock_change is None else stock_change

        # -------- Resolve Stock Code --------
        pattern = r'\/\.?([A-Z0-9]+)$'
        match = re.search(pattern, response.url)    # Extract stock code from url tail
        if match:
            stock_code = match.group(1)
        else:
            stock_code = "Unknown"

        # ------------ Stock Name ------------
        stock_name = "No name"
        if self.custom_settings["LANG"] == "CN" and stock_code in __stock_terms__.stock_CN:
            stock_name = __stock_terms__.stock_EN[stock_code]
        elif self.custom_settings["LANG"] == "EN" and stock_code in __stock_terms__.stock_EN:
            stock_name = __stock_terms__.stock_EN[stock_code]

        # --------- Data summarization ---------
        # Quote data
        quote_info_data = __quote_info__.resolve_quote_info_data(
            quote_info,
            self.custom_settings["LANG"],               # Language of attributes
            self.custom_settings["USE_EXACT_VALUES"]    # Use linguistic units or not
        )
        # Fundamental Data
        data = {
            "Index": self.index,
            "Stock Code": stock_code,
            "Stock Name CN": stock_name,
            "Market Status": market_status,
            "Current Price": cur_price,
            "Stock Change": stock_change,
            "Quote Info": quote_info_data,      # Quote info is compressed here
            "Current Time": time_str
        }

        self.stock_data.append(data)

        # Print result, deal with index
        self.index = print_result(data, txt_color)

        #save_data_to_excel(data,stock_name)
        print(data)


def save_data_to_excel(data, stock_name="Undefined"):
    file_name = stock_name+".xlsx"
    df = pd.DataFrame(data)
    df['Quote Info'] = df['Quote Info'].apply(pd.Series)  # 展开Quote Info列为多个列
    df.drop('Quote Info', axis=1, inplace=True)  # 删除"Quote Info"列
    df.to_excel(file_name, index=False)



# Print the results in the terminal
def print_result(data, txt_color):
    # Index and market status
    print('\033[0m' + str(data['Index'] + 1) + '. ' + data['Market Status'] + '\n')  # index

    # Fundamental Stock info
    print(
        txt_color +
        data['Stock Name CN'] + '(' + data['Stock Code'] + ')' + '\n' +
        'Current Price: ' + data['Current Price'] + '\n' +
        'Stock Change: ' + data['Stock Change']
    )

    # Stock quote info
    print_quote(data['Quote Info'])
    print('Current Time: ' + data['Current Time'])
    print('\n')

    # Put here because async
    return data['Index'] + 1


# Print quote info specifically
def print_quote(quote_info_data):
    print("-------Quotes-------")
    for key, value in quote_info_data.items():
        print(key + ": " + str(value))
    print('--------------------')


def run_spider():
    # Create CrawlerProcess instance
    process = CrawlerProcess()
    # Add a crawler to the process
    process.crawl(StockSpider)
    # Activate crawler
    process.start()


# Run this spider
run_spider()
