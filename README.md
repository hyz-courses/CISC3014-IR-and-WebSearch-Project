# CISC3014-IR-and-WebSearch-Project


## Rotten Tomatoes
&emsp; Rotten Tomatoes is a review-aggregation website for film and television in the U.S. 
It has its own ranking system of movies, with three tiers: Certified Fresh, Fresh, and Rotten. The goal of our project is to extract the main content of top 100+ list from RT, then make a query searcher based on the plot twists using TF-IDF model.


## First Crawler ```__get_movies__.py```
&emsp; In rottentomatoes.com, the movies collection is presented as a grid view of ``<div>`` container of attribute ``class="flex-container"``. Within each container, there's an ``<a>`` tab containing an ``href`` attribute that stores the sub-link to the movie details.

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
```

## Second Crawler
&emsp; Having the url list, we have the second crawler to crawl movie contents of each movie. One movie, with one url, which leads to one movie content, i.e., plots. We wrote a special function to read excel file and form an array of movie urls. These urls are encapsulated into a url array that's ' used as the ``start_urls`` attribute of the second crawler.

```python
def get_movie_url():
    # Read Excel file and do analysis
    file_path = './movie_list/movie_data.xlsx'
    movie_data = pd.read_excel(file_path)
    # Get URL
    url_series = movie_data['link']
    sub_urls = url_series.values

    # Header URL
    header_url = 'https://www.rottentomatoes.com'
    urls = np.array(sub_urls, dtype=object)
    urls_with_header = header_url + urls

    print(len(urls_with_header))
    return urls_with_header
```

&emsp; The second crawler calls this function to store the urls to be crawled. After this, it calls a ``start_requests()`` function to parse every url with the for-loop contained in it.
```python
    def start_requests(self):
        for url in self.start_urls:
            headers = {
                'User-Agent': self.get_random_user_agent()
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)
```

&emsp; The following is quite the same. We retrieve the title & contents of each crawler, and store them into an Excel file. Evidently, each movie corresponds to its own plot twists, in other words, articles. These articles will then be used to build a tf-idf search model.
```python
    def parse(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        genre = response.xpath("//span[@class='genre']/text()").get()
        genre = re.sub(r'\n|\s|\t', '', genre)

        content = response.xpath("//p[@slot='content']/text()").get()
        content = re.sub(r'\n|\t', '', content)

        data = {
            "title": title,
            "genre": genre,
            "content": content,
        }

        # Save data
        if self.custom_settings['SAVE_DATA']:
            __save_data__.save_data_to_excel(data, file_name="movie_content")

        print("\n title:" + title)
        print("\n genre:" + genre)
        print("\n content:\n" + content)
```


&emsp; The old one's still there, take a look:

## Some Ideas (Temporary):
&emsp; This project is temporarily given an idea of scraping stock information.
It would scrape 10 important indecies from Xueqiu.

&emsp; ```get_stock.py``` is the main file.
![Image](/screenshots/scr1.png)
