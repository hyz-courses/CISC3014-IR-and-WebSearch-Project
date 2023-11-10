# Please set the SAVE_DATA to True in order to record data.

import scrapy
import time
import re
import logging
import random
import pandas as pd
from scrapy.crawler import CrawlerProcess
import os

import __save_data__
# local imports
import __settings__


class MovieDetailCrawler(scrapy.Spider):
    name = 'rotten_tomatoes'
    allowed_domains = ['rottentomatoes.com']
    is_terminal_beautiful = False
    start_urls = __settings__.get_movie_url()
    custom_settings = {
        # Terminal settings: Ignore some warnings and logs
        # 'LOG_LEVEL': logging.ERROR,
        # 'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',

        # Local settings
        'LANG': 'EN',
        'USE_EXACT_VALUES': True,
        'SAVE_DATA': False,
        'ROUND_LEVEL': 3,
    }

    def start_requests(self):
        for url in self.start_urls:
            headers = {
                'User-Agent': self.get_random_user_agent()
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    # Use dynamic agent to avoid my IP to get banned
    def get_random_user_agent(self):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        ]
        return random.choice(user_agents)

    def parse(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        genre = response.xpath("//span[@class='genre']/text()").get()
        genre = re.sub(r'\n|\s|\t', '', genre)

        data = {
            "title": title,
            "genre": genre,
        }

        # Save data
        if self.custom_settings['SAVE_DATA']:
            __save_data__.save_data_to_excel(data, file_name="movie_genre")

        print("\n title:" + title)
        print("\n genre:" + genre)


def run_spider():
    # Create CrawlerProcess instance
    process = CrawlerProcess()
    # Add a crawler to the process
    process.crawl(MovieDetailCrawler)
    # Activate crawler
    process.start()


# Run this spider
run_spider()
