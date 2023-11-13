import math
import numpy as np
import pandas as pd

special_strings = {
    'WELCOME': 'Welcome to tfidf searcher!',
    'EMOJI': '（づ￣3￣）づ╭❤～',
    'R_CHEVRON': '>>>>>>>>>>> ',
    'L_CHEVRON': ' <<<<<<<<<<<',
}

special_scripts = {
    'BREAK_WHILE_LOOP': 'break()',
}

custom_settings = {
    'RM_COMMON_WORDS': True,
    'TYPE_SEARCH': True,
    'CONSOLE_LOG_PROCESS': False,
    'TOP_X': 5,
}


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


get_movie_url()