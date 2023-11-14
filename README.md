# CISC3014-IR-and-WebSearch-Project


## 1. Introduction to Rotten Tomatoes
&emsp; Rotten Tomatoes is a review-aggregation website for film and television in the U.S. 
It has its own ranking system of movies, with three tiers: Certified Fresh, Fresh, and Rotten. The goal of our project is to extract the main content of top 100+ list from RT, then make a query searcher based on the plot twists using TF-IDF model.


## 2. First Crawler ```__get_movies__.py```
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

## 3. Second Crawler ```__get_movie_detail__.py```
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

&emsp; The following is quite the same. We retrieve the title & contents of each crawler, and store them into an Excel file. Before storing each plot twist, we remove all the return and tab characters. 

&emsp; Evidently, each movie corresponds to its own plot twists, in other words, articles. These articles will then be used to build a tf-idf search model.

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

## 4. TF-IDF Model building
### 4.1. Tokenize each article into an array.

```python
def tokenize(input_str):
    # Define the splitting delimiters using regular expression
    rule = r'[\s\~\`\!\@\#\$\%\^\&\*\(\)\-\_\+\=\{\}\[\]\;\:\'\"\,\<\.\>\/\?\\|]+'
    re.compile(rule)

    # Turn all letters in the string into lowercase
    # This may contain empty member ''
    terms_ = []
    terms_ = terms_ + re.split(rule, input_str.lower())

    # Remove the empty member ''
    terms = []
    for term in terms_:
        if term != '':
            terms.append(term)

    last_word = terms[-1]
    # print("last_word: " + last_word)
    return terms
```

### 4.2. For each array, remove duplicates and form a term-frequency vector.
&emsp; The main part is the ``Counter()`` function, which counts duplicates and merge them together. For example, the query ``["the", "cake", "tastes", "like", "cake"]`` would be merged as ``{"the":1, "cake":2, "tastes":1, "like":1}``.

```python
def get_term_freq(movie_item):
    title = movie_item['title']
    content = movie_item['content']

    # Split content article into word array.
    term_array = tokenize(content)

    # Using word array, count term frequency.
    # Term frequency: term:key -> frequency:value
    movie_tf = Counter(term_array)
    movie_tf = dict(movie_tf)

    # Console logs
    if __settings__.custom_settings['CONSOLE_LOG_PROCESS']:
        print("\n>> " + title)
        # print(term_array)
        print(movie_tf)

    return movie_tf, title
```

### 4.3. Further combine tf vectors into tf matrix.
&emsp; We would first build the index of the matrix, which is an array of all the word that's ever existed in the queries. This requires to perform a set operation on all the tf vectors.

```python
def create_vocabulary(path="./movie_list/movie_content.xlsx"):
    movie_content = xls_to_df(file_path=path)

    # Initialize vocabulary set and term frequency array.
    vocab = set()
    term_freqs = []
    titles = []

    # For ALL movies:
    for index, row in movie_content.iterrows():
        tf, title = get_term_freq(row)  # Get its term frequency vector.
        titles.append(title)            # Merge terms into vocabulary first, and
        vocab.update(tf.keys())
        term_freqs.append(tf)           # Store in a unified term frequency matrix.
    vocab = list(vocab)

    # Console Log
    if __settings__.custom_settings['CONSOLE_LOG_PROCESS']:
        print("\n>>>> Vocab")
        print(vocab)

    return vocab, term_freqs, titles
```

&emsp; Besides, ``create_vocabulary()`` also preserves the sequence of movie titles, which will be used to match movie by their sequence IDs.

&emsp; Having the index of the matrix, we just insert data into the matrix. For each plot twist, i.e., each tf vector, for each word in the vector, traverse the index until the word is found, then insert it. 
```python
def create_tf_mat(path="./movie_list/movie_content.xlsx"):
    # First, extract vocabulary & term frequency 2D vector.
    vocab, term_freqs, titles = create_vocabulary(path=path)

    # Initializes term frequency matrix.
    term_freq_mat = pd.DataFrame(np.zeros((len(vocab), len(term_freqs))), index=vocab)

    # Insert data into the matrix.
    for index, term_freq in enumerate(term_freqs):
        for key, value in term_freq.items():
            term_freq_mat.loc[key, index] = value

    if __settings__.custom_settings['CONSOLE_LOG_PROCESS']:
        print('\n>>>> Term Frequency Matrix')
        print(term_freq_mat)

    return term_freq_mat, titles
```

&emsp; The rows are the frequency vector of each term, and the columns are frequency vector of each term in a specific plot twist.

```console
>>>> Term Frequency Matrix
           0    1    2    3    4    5    6    ...  110  111  112  113  114  115  116
facing     0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
follows    0.0  0.0  0.0  0.0  0.0  1.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
gabi       0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
looks      0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
pass       0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
...        ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...  ...
rebel      0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
wedding    0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  1.0  0.0  0.0  0.0
tales      0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
noises     0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
directing  0.0  0.0  0.0  0.0  0.0  0.0  0.0  ...  0.0  0.0  0.0  0.0  0.0  0.0  0.0
```

### 4.4. Using tf matrix, calculate inverse document frequency vector, then build tf-idf matrix.
&emsp; Inverse document frequency can be retrieved by:

\[\text{{IDF}}(t, D) = \log \left( \frac{{N}}{{\text{{df}}(t, D) + 1}} \right)\]

which yields to be:
```console
>>>> Inverse Document Frequency
[[2.38108697]
 [2.38108697]
 [2.38108697]
 ...
 [2.38108697]
 [2.38108697]
 [1.58739131]]
```
## 5. Search & Problems

&emsp; The old one's still there, take a look:

## Some Ideas (Temporary):
&emsp; This project is temporarily given an idea of scraping stock information.
It would scrape 10 important indecies from Xueqiu.

&emsp; ```get_stock.py``` is the main file.
![Image](/screenshots/scr1.png)
