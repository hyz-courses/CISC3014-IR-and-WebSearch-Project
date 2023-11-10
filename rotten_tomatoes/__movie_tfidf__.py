import numpy as np
import re
import pandas as pd
from collections import Counter


# Read Excel file into dataframe
def xls_to_df(file_path=""):
    df = pd.read_excel(file_path)
    return df


# Tokenize string into genre array
def tokenize(str):
    str_arr=re.split(',', str)
    return str_arr


# 
def processing(row):
    title = row['title']
    genre = row['genre']
    genre_arr = tokenize(genre)
    movie_tf = Counter(genre_arr)
    movie_tf = dict(movie_tf)
    print("\n>> " + title)
    print(genre_arr)
    print(movie_tf)
    return movie_tf


def create_vocabulary(path="./movie_list/movie_genre.xlsx"):
    movie_genre = xls_to_df(file_path=path)
    vocab = set()
    term_freqs = []
    for index, row in movie_genre.iterrows():
        tf = processing(row)
        vocab.update(tf.keys())
        term_freqs.append(tf)
    vocab = list(vocab)
    print("\n>>>> Vocab")
    print(vocab)

    return vocab, term_freqs


def create_tf_mat(path="./movie_list/movie_genre.xlsx"):
    vocab, term_freqs = create_vocabulary(path=path)
    term_freq_mat = pd.DataFrame(np.zeros((len(vocab), len(term_freqs))), index=vocab)
    for index, term_freq in enumerate(term_freqs):
        for key, value in term_freq.items():
            term_freq_mat.loc[key, index] = value

    return term_freq_mat

    print('\n>>>> Term Frequency Matrix')
    print(term_freq_mat)


def calc_idf(term_freq_mat):
    freq = np.count_nonzero(term_freq_mat, axis=1)
    idf = np.log(term_freq_mat.shape[1])/1+freq
    idf = np.reshape(idf, (len(idf), 1))

    print("\n>>>>IDF")
    print(idf)
    return idf

def create_tfidf_mat(term_freq_mat,idf_vector):
    tfidf_mat = term_freq_mat * idf_vector
    print("\n>>>>tf-idf")
    print(tfidf_mat)
    return tfidf_mat

def main():
    tf_mat = create_tf_mat(path='./movie_list/movie_genre.xlsx')
    idf_vector = calc_idf(tf_mat)
    #tfidf_mat = create_tfidf_mat(tf_mat, idf_vector)






main()
