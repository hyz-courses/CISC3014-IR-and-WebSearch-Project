import scrapy
import re
import logging
from scrapy.crawler import CrawlerProcess

class RTMovieCrawler(scrapy.Spider):
    name = 'Rotten Tomatoes'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ["https://www.rottentomatoes.com/browse/movies_at_home/sort:popular"]
    is_terminal_beautiful = True
    custom_settings = {
        # Terminal settings: Ignore some warnings and logs
        'LOG_LEVEL': logging.CRITICAL if is_terminal_beautiful is True else logging.ERROR,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',

        # Local settings
        'LANG': 'EN',
        'USE_EXACT_VALUES': True,
        'SAVE_DATA': True,
        'ROUND_LEVEL': 3,
    }

    movie_data=[]
    def parse(self, response):
        movie_list = response.xpath("//div[@class='flex-container']")
        for movie in movie_list:
            # Father element: Overall container
            score_container = movie.xpath(".//a[@data-track='scores']")
            # Title
            movie_title = score_container.xpath(".//span[@class='p--small']/text()").get()
            # Guardian method. Don't get useless message
            if movie_title is None:
                continue
            movie_title = re.sub(r"\n|\s","", movie_title)
            # Stream time
            stream_time = score_container.xpath(".//span[@class='smaller']/text()").get()
            stream_time = re.sub(r"\n|\s", "", stream_time)
            # Overall score container
            evaluation_scores = score_container.xpath(".//score-pairs-deprecated")
            # Four important scores
            aud_sentiment = evaluation_scores.xpath("@audiencesentiment").get()
            aud_score = evaluation_scores.xpath("@audiencescore").get()
            critics_sentiment = evaluation_scores.xpath("@criticssentiment").get()
            critics_score = evaluation_scores.xpath("@criticsscore").get()

            data = {
                "title": movie_title,
                "stream_time": stream_time,
                "audience sentiment": aud_sentiment,
                "audience score": aud_score,
                "critics sentiment": critics_sentiment,
                "critics score": critics_score
            }

            self.movie_data.append(data)

            print("--------------------")
            print(
                "title: " + movie_title + '\n' +
                "stream time: " + stream_time + '\n' +
                "audience sentiment: " + aud_sentiment + '\n' +
                "audience score: " + aud_score + '\n' +
                "critics sentiment: " + critics_sentiment + '\n' +
                "critics score: " + critics_score
            )


# 创建CrawlerProcess实例
process = CrawlerProcess()
# 添加爬虫到CrawlerProcess实例
process.crawl(RTMovieCrawler)
# 启动爬虫
process.start()
