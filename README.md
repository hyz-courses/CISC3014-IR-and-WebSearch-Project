# Project Exploration Instructions
### Course Title: CISC3014 
### Course Name: Information Retrieval and Web Search
### Project Title: Plot Search Using TF-IDF Model from Popular list of Rotten Tomatoes

### Group Members:
- Huang Yanzhen, DC126732
- Chen Zirui, DC127901

### Report & Presentation file:
[Report](Report%20and%20Presentation/CISC3014_Project_PDF.pdf)

## Instructions
**Notice: It is recommended to use PyCharm as the IDE.**
### 1. Please make sure you find the correct file:
- First Crawler: [``__get_movies__.py``](__get_movies__.py)
- Second Crawler: [``__get_movie_detail__.py``](__get_movie_detail__.py)
- Build TF-IDF Model and Perform query search: [``__movie_tfidf__.py``](__movie_tfidf__.py)

### 2. The following files are used to assist the project. **Please do not alter!**
- ``__settings__.py``: This is an integration of settings & dictionaries used in this project.
- ``__save_data__.py``: This is used to save data from the crawler into .xls files.
- The ``./movie_list`` directory is where the extracted data stored. Please don't alter any of the files in it.

### 3. If you want to play with searching:
- Please refer to [``__movie_tfidf__.py``](__movie_tfidf__.py).
- Search is done in the **console widow** of the IDE.
- Search whatever you want by typing the query in console! :)
```console
>> What do you want to search? how are you?
Searched for: "how are you?"
Top 5 relevant:
1.
ID: 22
Title: Barbie
Sim score: 0.15951288677347847
2.
ID: 8
Title: Talk to Me
Sim score: 0.10529535923061749
3.
ID: 52
Title: Renfield
Sim score: 0.10415622482978329
4.
ID: 47
Title: Infinity Pool
Sim score: 0.09977093851088208
5.
ID: 29
Title: Crossroads
Sim score: 0.05218335594877981
Search is complete!
```
- To stop the process, type ``break()`` in console.
```console
>> What do you want to search? break()

Process finished with exit code 0
```
- To list all movies, type ``ls`` in console.
```console
>> What do you want to search? ls
ID: 2
Title: Milli Vanilli

ID: 3
Title: No Hard Feelings

ID: 4
Title: Saw X

ID: 5
Title: The Exorcist: Believer

ID: 6
Title: The Burial

ID: 7
Title: Five Nights at Freddy's

...
```

### 4. If you want to run the crawler:
- Please make sure that the ``SAVE_DATA`` trigger in the custom settings in any of the crawler file 
(``__get_movies__.py`` or ``__get_movie_detail__.py``)
is set to ``False``. Otherwise, there will be duplicate rows of data since I have already stored some data into the excel file while preparing 
for the project. It should be pre-set to ``False`` anyways.


- If you run the first crawler ``__get_movies__.py``, please notice that the webpage content might be changed as time passed. The content 
used in the second crawler is based on the data retrieved before Oct. 31, 2023.

#### \_\_get_movies__.py or \_\_get_movie_detail__.py
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

### 5. If you want to inspect the content (e.g., the tf-idf matrix):
&emsp; Please head to ``__settings__.py`` and switch ``CONSOLE_LOG_PROCESS`` to ``True``. This allows the content to be
print in the console as soon as it is generated.
#### \_\_settings\_\_.py
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
https://github.com/YanzhenHuang/CISC3014-IR-and-WebSearch-Project
