import scrapy
import time
import re
import logging
import pandas as pd
from scrapy.crawler import CrawlerProcess
import os

class JobSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ['amazon.com']
    start_urls = ["https://www.amazon.com/s?k=information+retrieval+and+web+search&crid=5CY6QY7MJQ6A&sprefix=%2Caps%2C934&ref=nb_sb_ss_recent_2_0_recent"]
    is_terminal_beautiful = False
    custom_settings = {
        # Terminal settings: Ignore some warnings and logs
        #'LOG_LEVEL': logging.CRITICAL if is_terminal_beautiful is True else logging.ERROR,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',

        # Local settings
        'LANG': 'EN',
        'USE_EXACT_VALUES': True,
        'SAVE_DATA': True,
    }

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            #'Referer': 'https://bj.58.com/quanzhizhaopin/'
        }
        print("\n~~-----Crawler Started-----~~\n")
        # Crawl all the urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        job_list = response.xpath("//div[@class='main clearfix']")
        print(job_list)


def run_spider():
    # Create CrawlerProcess instance
    process = CrawlerProcess()
    # Add a crawler to the process
    process.crawl(JobSpider)
    # Activate crawler
    process.start()


# Run this spider
run_spider()
