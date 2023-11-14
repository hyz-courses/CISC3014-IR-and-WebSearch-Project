# CISC3014-IR-and-WebSearch-Project


## Rotten Tomatoes
&emsp; Rotten Tomatoes is a review-aggregation website for film and television in the U.S. 
It has its own ranking system of movies, with three tiers: Certified Fresh, Fresh, and Rotten. The goal of our project is to extract the main content of top 100+ list from RT, then make a query searcher based on the plot twists using TF-IDF model.


## First Crawler ```__get_movies__.py```
    &emsp; In rottentomatoes.com, the movies collection is presented as a grid view of <div> container of attribute ```class="flex-container"```. Within each container, there's an <a> tab containing an `href` attribute that stores the sub-link to the movie details.
    
    &emsp; Intuitively, we craw the entire list of movies by xpath:
    
    ```python
        movie_list = response.xpath("//div[@class='flex-container']")
    ```
    
    &emsp; Iterate this path. Within each path, we first get the <a> tag, and then retrieve its attributes:
    
    ```python
    score_container = movie.xpath(".//a[@data-track='scores']")score_link = score_container.xpath("@href").get()
    ``` 
    
    &emsp; Lastly, encapsulate this data into a data frame, and store in an excel file.
    
    ```python
                data = {                "title": movie_title,                "stream_time": stream_time,                'link': score_link,                "audience score": aud_score,                "critics score": critics_score,                "audience sentiment": bin_aud_sentiment,                "critics sentiment": bin_critics_sentiment,            }            # Append movie data... not            self.movie_data.append(data)            # Store the data in a new Excel file            self.start_urls.append("https://www.rottentomatoes.com/" + data['link'])            if self.custom_settings['SAVE_DATA']:                __save_data__.save_data_to_excel(data)
    ```
    
## Second Crawler


&emsp; The old one's still there, take a look:

## Some Ideas (Temporary):
&emsp; This project is temporarily given an idea of scraping stock information.
It would scrape 10 important indecies from Xueqiu.

&emsp; ```get_stock.py``` is the main file.
![Image](/screenshots/scr1.png)
