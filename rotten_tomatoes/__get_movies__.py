# Written by Huang Yanzhen at Oct 30, 2023

import scrapy
import re
import logging
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy import signals

# local imports
import __save_data__
import __get_movie_articles__

class RTMovieCrawler(scrapy.Spider):
    name = 'Rotten Tomatoes'
    allowed_domains = ['rottentomatoes.com']
    start_urls = ["https://www.rottentomatoes.com/browse/movies_at_home/sort:popular?page=21"]
    is_terminal_beautiful = True
    custom_settings = {
        # Terminal settings: Ignore some warnings and logs
        'LOG_LEVEL': logging.CRITICAL if is_terminal_beautiful is True else logging.ERROR,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',

        # Local settings
        'LANG': 'EN',
        'USE_EXACT_VALUES': True,
        'SAVE_DATA': False,     # Don't alter this!!! otherwise you'd create duplicate rows in the excel file
        'ROUND_LEVEL': 3,
    }

    # These aren't really useful yet...
    movie_data = []
    article_start_urls = []
    index = 1

    def parse(self, response):
        # Entire movie grid
        movie_list = response.xpath("//div[@class='flex-container']")
        for movie in movie_list:
            # Father element: Overall container
            score_container = movie.xpath(".//a[@data-track='scores']")
            score_link = score_container.xpath("@href").get()

            # Title
            movie_title = score_container.xpath(".//span[@class='p--small']/text()").get()
            # Guardian method. Don't get useless message
            if movie_title is None:
                continue
            movie_title = re.sub(r"\n|\s","", movie_title)      # In fact the movie title from rt is kinda sussy

            # Stream time
            stream_time = score_container.xpath(".//span[@class='smaller']/text()").get()
            stream_time = re.sub(r"\n|\s|Streaming", "", stream_time)

            # Overall score container
            evaluation_scores = score_container.xpath(".//score-pairs-deprecated")
            # Four important scores
            aud_sentiment = evaluation_scores.xpath("@audiencesentiment").get()
            aud_score = evaluation_scores.xpath("@audiencescore").get()
            critics_sentiment = evaluation_scores.xpath("@criticssentiment").get()
            critics_score = evaluation_scores.xpath("@criticsscore").get()

            # Processing data
            # Change negative/positive to binary expressions, which is a lot easier to cope with
            bin_aud_sentiment = 0 if aud_sentiment == 'negative' else 1
            bin_critics_sentiment = 0 if critics_sentiment == 'negative' else 1
            data = {
                "title": movie_title,
                "stream_time": stream_time,
                'link': score_link,
                "audience score": aud_score,
                "critics score": critics_score,
                "audience sentiment": bin_aud_sentiment,
                "critics sentiment": bin_critics_sentiment,
            }

            # Append movie data... not really useful, cuz i plug it into excel at each loop anyways
            self.movie_data.append(data)

            # Store the data in a new Excel file
            self.start_urls.append("https://www.rottentomatoes.com/" + data['link'])
            if self.custom_settings['SAVE_DATA']:
                __save_data__.save_data_to_excel(data)

            # Print beautiful data in console :)
            print("--------------------")
            print(
                str(self.index) + '\n' +
                "title: " + movie_title + '\n' +
                "stream time: " + stream_time + '\n' +
                "link:" + score_link + '\n' +
                "audience sentiment: " + aud_sentiment + '\n' +
                "audience score: " + aud_score + '\n' +
                "critics sentiment: " + critics_sentiment + '\n' +
                "critics score: " + critics_score
            )

            # This thread is async so I have to do this to omit race conditions
            self.index += 1


def run_process():
    process = CrawlerProcess()
    process.crawl(RTMovieCrawler)
    process.start()

run_process()



