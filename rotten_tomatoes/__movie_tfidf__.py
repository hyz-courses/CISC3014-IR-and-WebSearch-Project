import numpy as np
import re
import pandas as pd
from collections import Counter

# local imports
import __settings__


# Read Excel file into dataframe
def xls_to_df(file_path=""):
    df = pd.read_excel(file_path)
    return df


# ----------------- Document Part -------------------
# Tokenize string into word array.
# Input string is the content article of the movie.
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
    #print("last_word: " + last_word)
    return terms


# For a specific movie:
# Extract term frequency for its article.
# Example: {'in': 4, 'the': 6, 'retirement': 1}
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
    print("\n>> " + title)
    # print(term_array)
    print(movie_tf)

    return movie_tf, title


# Sum up all the term frequencies, create a vocab.
# Output: vocabulary, and a vector of tf vectors. (2D vector)
# 2D vector is like, [{'at':1, 'the':7}, {'susie':1, 'last':2}]
# using set merge.
def create_vocabulary(path="./movie_list/movie_content.xlsx"):
    movie_content = xls_to_df(file_path=path)

    # Initialize vocabulary set and term frequency array.
    vocab = set()
    term_freqs = []
    titles = []

    # For ALL movies:
    for index, row in movie_content.iterrows():
        # Get its term frequency vector.
        tf, title = get_term_freq(row)
        titles.append(title)
        # Merge terms into vocabulary first, and
        vocab.update(tf.keys())
        # Store in a unified term frequency matrix.
        term_freqs.append(tf)
    vocab = list(vocab)

    # Console Log
    print("\n>>>> Vocab")
    print(vocab)

    return vocab, term_freqs, titles


# Create term-frequency matrix
# Using vocabulary as index, and 2D vector value as values.
def create_tf_mat(path="./movie_list/movie_content.xlsx"):
    # First, extract vocabulary & term frequency 2D vector.
    vocab, term_freqs, titles = create_vocabulary(path=path)

    # Initializes term frequency matrix.
    term_freq_mat = pd.DataFrame(np.zeros((len(vocab), len(term_freqs))), index=vocab)

    # Insert data into the matrix.
    for index, term_freq in enumerate(term_freqs):
        for key, value in term_freq.items():
            term_freq_mat.loc[key, index] = value

    print('\n>>>> Term Frequency Matrix')
    print(term_freq_mat)

    return term_freq_mat, titles


# Create tf-idf matrix.
# Simply just multiply idf vector with tf matrix term-wise.
def create_tfidf_mat(term_freq_mat):
    # Inverse document frequency.
    # idf(term) = log(movie number) / 1 + (numer of movies containing this term)
    def calc_idf(term_freq_mat):
        doc_num = term_freq_mat.shape[1]
        freq = np.count_nonzero(term_freq_mat, axis=1)
        idf = np.log(doc_num) / (1 + freq)
        idf = np.reshape(idf, (len(idf), 1))

        # Filter words that are very common.
        # I can use nltk, but this is simpler.
        if __settings__.custom_settings['RM_COMMON_WORDS']:
            min_idf = np.log(doc_num) / (1 + doc_num)
            idf[idf == min_idf] = 0

        print("\n>>>> Inverse Document Frequency")
        print(idf)
        return idf

    idf_vector = calc_idf(term_freq_mat)
    tfidf_mat = term_freq_mat * idf_vector
    print("\n>>>> tf-idf Matrix")
    print(tfidf_mat)
    return tfidf_mat, idf_vector


# ----------------- Query Part -------------------

def cosine_compare(query, idf_vector, tfidf_mat):
    # Cosine Similarity
    def cosine(q, d):
        q = q.T  # Transpose vector to fit the dot op.
        cos_sim = np.dot(q, d) / (np.linalg.norm(q) * np.linalg.norm(d))
        return cos_sim.item()

    # Query tf-idf Vector
    def create_query_tfidf_vector(query, idf_vector):
        # Tokenizes query into term 2D vector
        q_term = query.lower().split(' ')  # lowercase, split by space
        q_term_freq = Counter(q_term)       # remove duplicates, make into dictionary
        q_term_freq = dict(q_term_freq)

        # Query tf vector
        q_tf_vector = pd.DataFrame(np.zeros((len(idf_vector), 1)), index=tfidf_mat.index)
        for key, value in q_term_freq.items():
            q_tf_vector.loc[key] = value

        # Query tfidf vector
        q_tfidf_vector = q_tf_vector * idf_vector
        return q_tfidf_vector

    # Compare query tfidf vector with all columns of tfidf_mat
    q_tfidf_vector = create_query_tfidf_vector(query, idf_vector)
    similarity_scores = []
    for doc in tfidf_mat.columns:
        doc_vector = tfidf_mat[doc]
        similarity_scores.append(cosine(q_tfidf_vector, doc_vector))

    return similarity_scores


def get_top_x_id(similarity_scores, top_x):
    # 获取前 top_x 个最高分数对应的索引
    sorted_similarity_scores = np.argsort(similarity_scores)[::-1]  # 按降序排序并获取索引
    top_x_scores = sorted_similarity_scores[:top_x]
    return top_x_scores


def get_top_x_names(similarity_scores, top_x, titles):
    top_x_scores = get_top_x_id(similarity_scores, top_x)
    top_x_names = []
    for score in top_x_scores:
        top_x_names.append(titles[score])
    return top_x_names


def search(search_queries, idf_vector, tfidf_mat, titles, top_x):
    print(" ------------- Totally " + str(len(search_queries)) + " search attempts! -------------")
    for index_search, query in enumerate(search_queries):
        similarity_scores = cosine_compare(query, idf_vector, tfidf_mat)
        top_10_id = get_top_x_id(similarity_scores, top_x)
        top_10_names = get_top_x_names(similarity_scores, top_x, titles)

        # Print Results
        print("\033[32m"+"\n"+str(index_search)+". Searched for: \"" + query + "\"")
        print("Top " + str(top_x) + " relevant:"+"\033[0m")
        for index_top in range(0, len(top_10_id)):
            print(str(index_top+1) + ".")
            print("ID: " + str(top_10_id[index_top] + 2))
            print("Title: " + str(top_10_names[index_top]))
            print("Sim score: " + str(similarity_scores[top_10_id[index_top]]))


# Problems
# 1. Sensitive to common words: the, a, an, they, theirs, city, etc.
# Solution: Filter words with min idf
# 2. Bad typo-tolerance: Typo may cause an overflow of array.
# Solution: Further machine learning techniques....

def main():
    tf_mat, titles = create_tf_mat(path='./movie_list/movie_content.xlsx')
    tfidf_mat, idf_vector = create_tfidf_mat(tf_mat)
    search_queries = [
        'discover how important',               # back of 29
        'on the brink of losing her',           # head of 3
        'Samuel suddenly vanishes',
        'more to her father',   # back of 111
        'retirement plan',   # head of 111
        'russell bufalino',     # 102
        'retired glamorous',   # 17
        'retired glamorous city',   # ought to be 17, but the word "city" is too strong...
        'After rescuing a young boy from ruthless child traffickers',
        'Romance about Maja',
        'while the OwNeR of the nearby theme park',
        'former baby sitter',         # 27
        #'typo test lalalala',
    ]

    search(search_queries, idf_vector, tfidf_mat, titles, 3)


main()
