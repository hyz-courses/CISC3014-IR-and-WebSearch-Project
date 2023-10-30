import scrapy
import re
import logging
import pandas as pd
from scrapy.crawler import CrawlerProcess

# local imports
import __save_data__


class RTMovieArticleCrawler(scrapy.Spider):
    name = 'Rotten Tomatoes'
    allowed_domains = ['rottentomatoes.com']
    start_urls = [
        # "https://www.rottentomatoes.com/m/pain_hustlers"
    ]
    is_terminal_beautiful = True
    custom_settings = {
        # Terminal settings: Ignore some warnings and logs
        'LOG_LEVEL': logging.CRITICAL if is_terminal_beautiful is True else logging.ERROR,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',

        # Local settings
        'LANG': 'EN',
        'USE_EXACT_VALUES': True,
        'SAVE_DATA': False,
        'ROUND_LEVEL': 3,
    }

    # Constructor.
    # This is written to define start urls from outside of this class.
    def __init__(self, *args, **kwargs):
        super(RTMovieArticleCrawler, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', [])

    def start_requests(self):
        print("\n~~-----Cralwer started-----~~\n")

        # Crawl all the urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Movie article
        movie_article = response.xpath("//p[@data-qa='movie-info-synopsis']/text()").get()
        movie_article = re.sub(r"\t|\n","", movie_article)
        # Tokenize article into words
        terms = tokenize(movie_article)
        print(terms)



def tokenize(article):
    rule = r'[\s\~\`\!\@\#\$\%\^\&\*\(\)\-\_\+\=\{\}\[\]\;\:\'\"\,\<\.\>\/\?\\|]+'
    re.compile(rule)

    terms_ = []
    terms_ = terms_ + re.split(rule, article.lower())

    terms = []

    for term in terms_:
        if term != '':
            terms.append(term)
    return terms


def run_process(start_urls):
    # 创建CrawlerProcess实例
    process = CrawlerProcess()
    # 添加爬虫到CrawlerProcess实例
    process.crawl(RTMovieArticleCrawler)
    # 启动爬虫
    process.start()

# run_process()


