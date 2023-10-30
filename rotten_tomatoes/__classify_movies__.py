import math
import pandas as pd

filepath = './movie_list/movie_data.xlsx'
movie_data = pd.read_excel(filepath)
aud_score = movie_data['audience score']
critics_score = movie_data['critics score']
aud_sentiment = movie_data['audience sentiment']
critics_sentiment = movie_data['critics sentiment']


# Input binary condition and binary target, output information gain
def binary_analysis(condition, target):
    def get_entropy(a, b):
        total = a + b
        # Deal with divide by 0 problem
        a_ratio = a / total if total != 0 else 0
        b_ratio = b / total if total != 0 else 0

        # Deal with divide by 0 problem
        a_log_a = a_ratio * math.log10(a_ratio) if a_ratio != 0 else 0
        b_log_b = b_ratio * math.log10(b_ratio) if b_ratio != 0 else 0

        # Finally, calculate the entropy.....
        entropy = (-1) * (a_log_a - b_log_b)
        return entropy

    negative = []       # negative conditions
    positive = []       # positive conditions

    # go through every row in the condition
    for index, row in enumerate(condition):
        if row == 0:
            negative.append(index)
        if row == 1:
            positive.append(index)

    # Focus on condition negative
    neg_neg = 0     # target negative
    neg_pos = 0     # target positive
    for index in negative:
        if target[index] == 0:
            neg_neg += 1
        if target[index] == 1:
            neg_pos += 1

    # Focus on condition positive
    pos_neg = 0     # target negative
    pos_pos = 0     # target positive
    for index in positive:
        if target[index] == 0:
            neg_neg += 1
        if target[index] == 1:
            neg_pos += 1

    # Compute entropy
    num_neg_total = len(negative)               # Total num of negative
    num_pos_total = len(positive)               # Total num of positive
    num_total = num_neg_total + num_pos_total   # Total num of records

    neg_ratio = num_neg_total / num_total if num_total != 0 else 0      # Negative ratio
    pos_ratio = num_pos_total / num_total if num_total != 0 else 0      # Positive ratio

    e_before_class = get_entropy(num_neg_total, num_pos_total)      # Entropy before classification

    e_neg = get_entropy(neg_neg, neg_pos)       # Entropy of classification of negative
    e_pos = get_entropy(pos_neg, pos_pos)       # Entropy of classification of positive

    info_gain = e_before_class - (neg_ratio * e_neg + pos_ratio * e_pos)        # Total information gain

    # Print in console
    print(
        '\n\n' +
        ">>>>>>>>>> Binary Analysis <<<<<<<<<<" + '\n' +
        "\n|---------- Records ----------|"
    )
    print(
        "Total num of condition '0's: " + str(num_neg_total) + '\n' +
        "Total num of condition '1's: " + str(num_pos_total) + '\n' +
        "Negative ratio: " + str(neg_ratio) + '\n' +
        "Positive ratio: " + str(pos_ratio) + '\n' +
        "Total num: " + str(num_total)
    )
    print("\n|---------- Entropy ----------|")
    wow_eneg = " (wow!)" if e_neg == 0 else ""
    wow_epos = " (wow!)" if e_pos == 0 else ""
    print(
        "Entropy of parent: " + str(e_before_class) + '\n' +
        "Entropy of class '0': " + str(e_neg) + wow_eneg + '\n' +
        "Entropy of class '1': " + str(e_pos) + wow_epos
    )
    print("\n|--------- Info Gain ---------|")
    wow = " (wow!)" if info_gain == 0 else ""
    print("Information gain: " + str(info_gain) + wow)

    return info_gain

# Input numeric condition and binary target, output information gain
def numeric_analysis(condition, target):
    mean_val = condition.mean()

    # Print result
    print(
        '\n\n' +
        ">>>>>>>>>> Numeric Analysis <<<<<<<<<<" + '\n' +
        "|---------- Records ----------|"
    )





#print(aud_sentiment)
binary_analysis(aud_sentiment, critics_sentiment)
numeric_analysis(aud_score, critics_sentiment)
