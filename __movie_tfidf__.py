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
    # print("last_word: " + last_word)
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
    if __settings__.custom_settings['CONSOLE_LOG_PROCESS']:
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

    if __settings__.custom_settings['CONSOLE_LOG_PROCESS']:
        print('\n>>>> Term Frequency Matrix')
        print(term_freq_mat)

    return term_freq_mat, titles


# Create tf-idf matrix.
# Simply just multiply idf vector with tf matrix term-wise.
def create_tfidf_mat(term_freq_mat):
    # Inverse document frequency.
    # idf(term) = log(movie number) / 1 + (numer of movies containing this term)
    def calc_idf(term_freq_mat):
        doc_num = term_freq_mat.shape[1]                    # Number of movies
        freq = np.count_nonzero(term_freq_mat, axis=1)      # Doc frequency

        # Inverse document frequency
        idf = np.log(doc_num) / (1 + freq)
        idf = np.reshape(idf, (len(idf), 1))

        # Filter words that are very common.
        # I can use nltk, but this is simpler.
        if __settings__.custom_settings['RM_COMMON_WORDS']:
            min_idf = np.log(doc_num) / (1 + doc_num)
            idf[idf == min_idf] = 0

        # Console Log
        if __settings__.custom_settings['CONSOLE_LOG_PROCESS']:
            print("\n>>>> Inverse Document Frequency")
            print(idf)
        return idf

    # Inverse Document Frequency
    idf_vector = calc_idf(term_freq_mat)
    # tf-idf matrix
    tfidf_mat = term_freq_mat * idf_vector
    # Console Log
    if __settings__.custom_settings['CONSOLE_LOG_PROCESS']:
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
        q_term = tokenize(query)
        q_term_freq = Counter(q_term)  # remove duplicates, make into dictionary
        q_term_freq = dict(q_term_freq)

        # Query tf vector
        q_tf_vector = pd.DataFrame(np.zeros((len(idf_vector), 1)), index=tfidf_mat.index)
        for key, value in q_term_freq.items():
            q_tf_vector.loc[key] = value

        # Query tfidf vector
        # Error handling: Size doesn't mach
        if q_tf_vector.shape[0] != idf_vector.shape[0] or q_tf_vector.shape[1] != idf_vector.shape[1]:
            return q_tf_vector, False
        # Size matches
        q_tfidf_vector = q_tf_vector * idf_vector
        return q_tfidf_vector, True

    # Compare query tfidf vector with all columns of tfidf_mat
    q_tfidf_vector, is_success = create_query_tfidf_vector(query, idf_vector)
    # Error handling: Size don't match
    if not is_success:
        return [], False
    # Size matches, continue.
    similarity_scores = []
    for doc in tfidf_mat.columns:
        doc_vector = tfidf_mat[doc]
        similarity_scores.append(cosine(q_tfidf_vector, doc_vector))

    return similarity_scores, True


def get_top_x_id(similarity_scores, top_x):
    # Fetch top x most relevant.
    # Sort array into descending order. Keep the original index.
    sorted_similarity_scores = np.argsort(similarity_scores)[::-1]

    # Num of records can't exceed maximum
    num_of_records = len(similarity_scores)
    if top_x > num_of_records:
        top_x = num_of_records

    top_x_id = sorted_similarity_scores[:top_x]
    return top_x_id


def get_top_x_names(similarity_scores, top_x, titles):
    top_x_id = get_top_x_id(similarity_scores, top_x)
    top_x_names = []
    for id in top_x_id:
        top_x_names.append(titles[id])
    return top_x_names


def search(search_queries, idf_vector, tfidf_mat, titles, top_x):
    if len(search_queries) > 1:
        print("------------- Totally " + str(len(search_queries)) + " search attempts! -------------")

    for index_search, query in enumerate(search_queries):
        # Scores, in sequence of movies
        similarity_scores, is_success = cosine_compare(query, idf_vector, tfidf_mat)
        # Exception: Query size doesn't fit!
        if not is_success:
            print("\033[31m$ Warning: Word not exist, try another one.\033[0m\n")
            return

        top_x_id = get_top_x_id(similarity_scores, top_x)   # Sort from high to low, return index.
        top_x_names = get_top_x_names(similarity_scores, top_x, titles)     # Use index to retrieve title.

        # Print Results
        # Title
        index = str(index_search) + ". " if len(search_queries) > 1 else ""
        print("\033[32m" + index + "Searched for: \"" + query + "\"\n" +
              "Top " + str(top_x) + " relevant:" + "\033[0m"
              )

        # Topx x result!
        for index_top in range(0, len(top_x_id)):
            # index_top -> top_x_id -> score
            this_similarity_score = similarity_scores[top_x_id[index_top]]
            if this_similarity_score == 0:
                print("\033[33m\n$ Warning: No more related movies!!\033[0m")
                break
            print(str(index_top + 1) + ".\n" +
                  "ID: " + str(top_x_id[index_top] + 2) + "\n" +
                  "Title: " + str(top_x_names[index_top]) + "\n" +
                  "Sim score: " + str(this_similarity_score)
                  )
        print("\033[32mSearch is complete!\033[0m")


# Problems
# 1. Sensitive to common words: the, a, an, they, theirs, city, etc.
# Solution: Filter words with min idf
# 2. Bad typo-tolerance: Typo may cause an overflow of array.
# Solution: Further machine learning techniques....

# Presentation (Regular):
# 1. Type in "ls" to show all movies
# 2. Type in some common words, like "city", "love", "true love" and "boy".
# 3. Type in some scripts known in a movie.

# Presentation (Problems):
# 1. Purposely make a typo, yield an error.
# 2. Use "theme park" to display the cascading feature.
# 3. Use "six year old" and "year old" to show the common word's problem.
# 4. Use "discover how important" to show the sequence problem.

def main():
    # Term frequency matrix & title array.
    tf_mat, titles = create_tf_mat(path='./movie_list/movie_content.xlsx')
    # tf-idf matrix & idf vector.
    tfidf_mat, idf_vector = create_tfidf_mat(tf_mat)
    # top x
    _top_x = __settings__.custom_settings['TOP_X']
    # Default search queries.
    search_queries = [
        'discover how important',  # back of 29
        'on the brink of losing her',  # head of 3
        'Samuel suddenly vanishes',
        'more to her father',  # back of 111
        'retirement plan',  # head of 111
        'russell bufalino',  # 102
        'retired glamorous',  # 17
        'retired glamorous city',  # ought to be 17, but the word "city" is too strong...
        'After rescuing a young boy from ruthless child traffickers',
        'Romance about Maja',
        'while the OwNeR of the nearby theme park',
        'former baby sitter',  # 27
        # 'typo test lalalala',
    ]

    if __settings__.custom_settings['TYPE_SEARCH']:
        # Welcome Screen!
        print(
            "\n\033[32m" +
            __settings__.special_strings['R_CHEVRON'] +
            __settings__.special_strings['WELCOME'] +
            __settings__.special_strings['EMOJI'] +
            __settings__.special_strings['L_CHEVRON'] +
            "\033[0m"
        )
        # Don't halt when a search is done. Do some more.
        while True:
            query_arr_encap = []
            input_query = input("\n>> What do you want to search? ")  # User input a search query.
            # Read user inputs.
            if input_query == __settings__.special_scripts['BREAK_WHILE_LOOP']:
                # A means to halt the while-loop.
                break
            if input_query == __settings__.special_scripts['LIST_ALL']:
                # List all movies
                for index, title in enumerate(titles):
                    print("ID: " + str(index+2) + "\n" + "Title: " + title + "\n")
                continue

            # Search the user input query
            query_arr_encap.append(input_query)
            search(query_arr_encap, idf_vector, tfidf_mat, titles, _top_x)  # Perform search
    else:
        search(search_queries, idf_vector, tfidf_mat, titles, _top_x)


main()
