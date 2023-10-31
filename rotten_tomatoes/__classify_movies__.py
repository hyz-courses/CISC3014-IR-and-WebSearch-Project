import math
import pandas as pd


# Input binary condition and binary target, output information gain
def binary_analysis(condition, target, cond_name="Binary Analysis"):
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

    id_cond_neg = []       # negative conditions
    id_cond_pos = []       # positive conditions
    num_targ_neg = 0       # num of negative targets
    num_targ_pos = 0       # num of positive targets

    # go through every row in the condition
    for index, row in enumerate(condition):
        if row == 0:
            id_cond_neg.append(index)
        if row == 1:
            id_cond_pos.append(index)

    # Focus on condition negative
    neg_neg = 0     # target negative
    neg_pos = 0     # target positive
    for index in id_cond_neg:
        if target[index] == 0:
            neg_neg += 1
            num_targ_neg += 1
        if target[index] == 1:
            neg_pos += 1
            num_targ_pos += 1

            # Focus on condition positive
    pos_neg = 0     # target negative
    pos_pos = 0     # target positive
    for index in id_cond_pos:
        if target[index] == 0:
            neg_neg += 1
            num_targ_neg += 1
        if target[index] == 1:
            neg_pos += 1
            num_targ_pos += 1

    # Compute entropy
    # Parent entropy
    num_total = num_targ_neg + num_targ_pos       # Total num of records
    neg_ratio = num_targ_neg / num_total if num_total != 0 else 0      # Target negative
    pos_ratio = num_targ_pos / num_total if num_total != 0 else 0      # Target positive
    e_parent = get_entropy(num_targ_neg, num_targ_pos)

    # Child entropy
    e_neg = get_entropy(neg_neg, neg_pos)       # Condition negative
    e_pos = get_entropy(pos_neg, pos_pos)       # Condition positive

    # Information gain
    info_gain = e_parent - (neg_ratio * e_neg + pos_ratio * e_pos)        # Total information gain

    # Print in console
    print(
        '\n\n' +
        ">>>>>>>>>> " + cond_name + " <<<<<<<<<<" + '\n' +
        "|---------- Records ----------|"
    )
    print(
        "Total num of condition '0's: " + str(num_targ_neg) + '\n' +
        "Total num of condition '1's: " + str(num_targ_pos) + '\n' +
        "Negative ratio: " + str(neg_ratio) + '\n' +
        "Positive ratio: " + str(pos_ratio) + '\n' +
        "Total num: " + str(num_total)
    )
    print("|---------- Entropy ----------|")
    wow_eneg = " (wow!)" if e_neg == 0 else ""
    wow_epos = " (wow!)" if e_pos == 0 else ""
    print(
        "Entropy of parent: " + str(e_parent) + '\n' +
        "Entropy of class '0': " + str(e_neg) + wow_eneg + '\n' +
        "Entropy of class '1': " + str(e_pos) + wow_epos
    )
    print("|--------- Info Gain ---------|")
    wow = " (wow!)" if info_gain == 0 else ""
    print("Information gain: " + str(info_gain) + wow)

    return info_gain


# Input numeric condition and binary target, output information gain
def numeric_analysis(condition, target, cond_name="Numeric Analysis"):

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

    id_cond_small = []          # condition small
    id_cond_medium = []         # condition medium
    id_cond_large = []          # condition large


    # Categorize into 3 conditions: small, medium, and large
    for index, row in enumerate(condition):
        if row < left_mean:
            id_cond_small.append(index)
        elif row > right_mean:
            id_cond_large.append(index)
        else:
            id_cond_medium.append(index)

    #
    [s_neg, s_pos] = count(id_cond_small)
    [m_neg, m_pos] = count(id_cond_medium)
    [l_neg, l_pos] = count(id_cond_large)

    # Compute Entropy
    # Compute number of target neg & pos
    num_targ_neg = 0
    num_targ_pos = 0
    for target_value in target:
        if target_value == 0:
            num_targ_neg += 1
        else:
            num_targ_pos += 1

    # Parent entropy
    num_total = num_targ_neg + num_targ_pos
    e_parent = get_entropy(num_targ_neg, num_targ_pos)

    # Child entropy
    num_small = len(id_cond_small)
    num_medium = len(id_cond_medium)
    num_large = len(id_cond_large)

    ratio_small = num_small / num_total if num_total != 0 else 0
    ratio_medium = num_medium / num_total if num_total != 0 else 0
    ratio_large = num_large / num_total if num_total != 0 else 0

    s_log_s = ratio_small * math.log10(ratio_small) if ratio_small !=0 else 0
    m_log_m = ratio_medium * math.log10(ratio_medium) if ratio_medium != 0 else 0
    l_log_l = ratio_large * math.log10(ratio_large) if ratio_large != 0 else 0

    # Child entropy
    e_small = get_entropy(s_neg, s_pos)
    e_medium = get_entropy(m_neg, m_pos)
    e_large = get_entropy(l_neg, l_pos)

    # Info gain
    info_gain = e_parent - (ratio_small * s_log_s + ratio_medium * m_log_m + ratio_large * l_log_l)

    # Print result
    print(
        '\n\n' +
        ">>>>>>>>>> " + cond_name + " <<<<<<<<<<" + '\n' +
        "|---------- Records ----------|" + '\n' +
        "Total num of small: " + str(num_small) + '\n' +
        "Total num of medium: " + str(num_medium) + '\n' +
        "Total num of large:" + str(num_large) + '\n' +
        "Total record num: " + str(num_total) + '\n' +
        "|---------- Entropy ----------|" + '\n' +
        "Parent Entropy: " + str(e_parent) + '\n' +
        "Entropy of small: " + str(e_small) + '\n' +
        "Entropy of medium: " + str(e_medium) + '\n' +
        "Entropy of large: " + str(e_large) + '\n' +
        "|--------- Info Gain ---------|" + '\n' +
        "Information Gain: " + str(info_gain) + '\n'
    )

    return info_gain


# Hybrid analysis, combining numeric and binary analysis.
def hybrid_analysis(condition, target, is_binary=True, name="Analysis Name"):
    if is_binary:
        info_gain = binary_analysis(condition, target, name)
    else:
        info_gain = numeric_analysis(condition, target, name)
    return info_gain

# ------------------------- Classification Part ---------------------------

# Read Excel file and do analysis
filepath = './movie_list/movie_data.xlsx'
movie_data = pd.read_excel(filepath)
# Conditions
aud_score = movie_data['audience score']
critics_score = movie_data['critics score']
aud_sentiment = movie_data['audience sentiment']
# Target
critics_sentiment = movie_data['critics sentiment']


# Get info gain from the three conditions
ig_aud_sentiment = hybrid_analysis(aud_sentiment, critics_sentiment, True, "Audience Sentiment")    # Audience sentiment
ig_aud_score = hybrid_analysis(aud_score, critics_sentiment, False, "Audience Score")               # Audience score
ig_critics_score = hybrid_analysis(critics_score, critics_sentiment, False, "Critics Score")        # Critics score

# Sort the three conditions from high to low
variables = [
    ('Audience Sentiment', ig_aud_sentiment),
    ('Audience Score', ig_aud_score),
    ('Critics Score', ig_critics_score)
]

variables_sorted = sorted(variables, key=lambda x: x[1], reverse=True)

# Print the three values:
print("~~~~~~~~~~~ Info Gain Ranking ~~~~~~~~~~~")
for i, (name, value) in  enumerate(variables_sorted):
    print(f"{i+1}. Info Gain from {name}: {value}")





