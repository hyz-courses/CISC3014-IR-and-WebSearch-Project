import math
import pandas as pd

filepath = './movie_list/movie_data.xlsx'
movie_data = pd.read_excel(filepath)
aud_score = movie_data['audience score']
critics_score = movie_data['critics score']
aud_sentiment = movie_data['audience sentiment']
critics_sentiment = movie_data['critics sentiment']


# Input binary condition and binary target, output information gain
def binary_analysis(condition, target, name="Binary Analysis"):
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
    # Parent entropy
    num_neg_total = len(negative)               # Total num of negative
    num_pos_total = len(positive)               # Total num of positive
    num_total = num_neg_total + num_pos_total   # Total num of records

    neg_ratio = num_neg_total / num_total if num_total != 0 else 0      # Negative ratio
    pos_ratio = num_pos_total / num_total if num_total != 0 else 0      # Positive ratio

    e_before_class = get_entropy(num_neg_total, num_pos_total)      # Entropy before classification

    # Child entropy
    e_neg = get_entropy(neg_neg, neg_pos)       # Entropy of classification of negative
    e_pos = get_entropy(pos_neg, pos_pos)       # Entropy of classification of positive

    # Information gain
    info_gain = e_before_class - (neg_ratio * e_neg + pos_ratio * e_pos)        # Total information gain

    # Print in console
    print(
        '\n\n' +
        ">>>>>>>>>> " + name + " <<<<<<<<<<" + '\n' +
        "|---------- Records ----------|"
    )
    print(
        "Total num of condition '0's: " + str(num_neg_total) + '\n' +
        "Total num of condition '1's: " + str(num_pos_total) + '\n' +
        "Negative ratio: " + str(neg_ratio) + '\n' +
        "Positive ratio: " + str(pos_ratio) + '\n' +
        "Total num: " + str(num_total)
    )
    print("|---------- Entropy ----------|")
    wow_eneg = " (wow!)" if e_neg == 0 else ""
    wow_epos = " (wow!)" if e_pos == 0 else ""
    print(
        "Entropy of parent: " + str(e_before_class) + '\n' +
        "Entropy of class '0': " + str(e_neg) + wow_eneg + '\n' +
        "Entropy of class '1': " + str(e_pos) + wow_epos
    )
    print("|--------- Info Gain ---------|")
    wow = " (wow!)" if info_gain == 0 else ""
    print("Information gain: " + str(info_gain) + wow)

    return info_gain

# Input numeric condition and binary target, output information gain
def numeric_analysis(condition, target, name="Numeric Analysis"):

    # Count positive and negative smaples within a conditional class
    def count(cond_class):
        sample_neg = 0
        sample_pos = 0
        for target_index in cond_class:
            if target[target_index] == 0:
                sample_neg += 1
            elif target[target_index] == 1:
                sample_pos += 1

        return sample_neg, sample_pos

    # Calculate entropy of a classification
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


    # Defines left mean and right mean
    mean_val = condition.mean()
    left_mean = (condition.min() + mean_val) / 2
    right_mean = (condition.max() + mean_val) / 2

    small = []
    medium = []
    large = []

    # Categorize into 3 conditions: small, medium, and large
    for index, row in enumerate(condition):
        if row < left_mean:
            small.append(index)
        elif row > right_mean:
            large.append(index)
        else:
            medium.append(index)

    #
    [s_neg, s_pos] = count(small)
    [m_neg, m_pos] = count(medium)
    [l_neg, l_pos] = count(large)


    # Compute Entropy
    # Parent entropy
    num_small = len(small)
    num_medium = len(medium)
    num_large = len(large)
    num_total = num_small + num_medium + num_large
    ratio_small = num_small / num_total if num_total != 0 else 0
    ratio_medium = num_medium / num_total if num_total != 0 else 0
    ratio_large = num_large / num_total if num_total != 0 else 0

    s_log_s = ratio_small * math.log10(ratio_small) if ratio_small !=0 else 0
    m_log_m = ratio_medium * math.log10(ratio_medium) if ratio_medium != 0 else 0
    l_log_l = ratio_large * math.log10(ratio_large) if ratio_large != 0 else 0

    e_parent = (-1) * (s_log_s + m_log_m + l_log_l)

    # Child entropy
    e_small = get_entropy(s_neg, s_pos)
    e_medium = get_entropy(m_neg, m_pos)
    e_large = get_entropy(l_neg, l_pos)

    # Info gain
    info_gain = e_parent - (ratio_small * s_log_s + ratio_medium * m_log_m + ratio_large * l_log_l)





    # Print result
    print(
        '\n\n' +
        ">>>>>>>>>> " + name + " <<<<<<<<<<" + '\n' +
        "|---------- Records ----------|" + '\n' +
        "Total num of small: " + str(num_small) + '\n' +
        "Total num of medium: " + str(num_medium) + '\n' +
        "Total num of large:" + str(num_large) + '\n' +
        "Total record num: " + str(num_total) + '\n' +
        "Parent Entropy: " + str(e_parent) + '\n' +
        "|---------- Entropy ----------|" + '\n' +
        "Entropy of small: " + str(e_small) + '\n' +
        "Entropy of medium: " + str(e_medium) + '\n' +
        "Entropy of large: " + str(e_large) + '\n' +
        "|--------- Info Gain ---------|" + '\n' +
        "Information Gain: " + str(info_gain) + '\n'
    )





#print(aud_sentiment)
binary_analysis(aud_sentiment, critics_sentiment, "Audience Sentiment")
numeric_analysis(aud_score, critics_sentiment, "Audience Score")
numeric_analysis(critics_score, critics_sentiment, "Critics Score")
