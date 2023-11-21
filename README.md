# Project Exploration Instructions
### Course Name: CISC3014 Information Retrieval and Web Search
### Project Title: Plot Search Using TF-IDF Model from Popular list of Rotten Tomatoes

### Group Members:
- Huang Yanzhen, DC126732
- Chen Zirui, DC127901

## Instructions
**Notice: It is recommended to use PyCharm as the IDE.**
### 1. Please make sure you find the correct file:
- First Crawler: ``__get_movies__.py``
- Second Crawler: ``__get_movie_detail__.py``
- Build TF-IDF Model and Perform query search: ``__movie_tfidf__.py``

### 2. The following files are used to assist the project. **Please do not alter!**
- ``__settings__.py``: This is an integration of settings & dictionaries used in this project.
- ``__save_data__.py``: This is used to save data from the crawler into .xls files.
- The ``./movie_list`` directory is where the extracted data stored. Please don't alter any of the files in it.

### 3. If you want to play with searching:
- Please refer to the ``__movie_tfidf__.py`` file!
- Search whatever you want! :)
- To stop the process, type ``break()``.
- To list all movies, type ``ls``.

### 4. If you want to run the crawler:
- Please make sure that the ``SAVE_DATA`` trigger in the custom settings in either of the crawler file
is set to ``False``. Otherwise, there will be duplicate rows of data since I have already stored some data into the excel file while preparing 
for the project. It should be pre-set to ``False`` anyways.


- If you run the first crawler, please notify that the webpage content might be changed as time passed. The content 
used in the second crawler is based on the data retrieved before Oct. 31, 2023.

#### __get_movies__.py or __get_movie_detail__.py
```python
    custom_settings = {
        # Terminal settings: Ignore some warnings and logs
        'LOG_LEVEL': logging.CRITICAL if is_terminal_beautiful is True else logging.ERROR,
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',

        # Local settings
        'LANG': 'EN',
        'USE_EXACT_VALUES': True,
        'SAVE_DATA': False,     # Please make sure that this switch is False!
        'ROUND_LEVEL': 3,
    }
```

### 5. If you want to inspect the content of the like the tf-idf matrix:
&emsp; Please head to ``__settings__.py`` and switch ``CONSOLE_LOG_PROCESS`` to ``True``. This allows the content to be
print in the console as soon as it is generated.
#### __settings__.py
```python
custom_settings = {
    'RM_COMMON_WORDS': True,
    'TYPE_SEARCH': True,
    'CONSOLE_LOG_PROCESS': False,   # Please set this to true.
    'TOP_X': 5,     # Alter me to get different numbers of records.
}
```
&emsp; Also, you can alter how many records you'd like to get each time you perform a search by altering the ``TOP_X`` attribute.
This number can't exceed 117 since there's only 117 movies to be searched. If it does exceed however, the program will return only the 
first 117 records at maximum.

### 6. If you encounter any problem, please kindly refer to the GitHub repository:
https://github.com/YanzhenHuang/CISC3014-IR-and-WebSearch-Project/tree/main/rotten_tomatoes