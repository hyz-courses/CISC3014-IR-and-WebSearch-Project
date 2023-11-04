import math
import pandas as pd


# Compute Entropy of a node
def get_entropy(a, b):
    total = a + b
    # Deal with divide by 0 problem
    a_ratio = a / total
    b_ratio = b / total

    # Deal with divide by 0 problem
    a_log_a = a_ratio * math.log10(a_ratio) if a_ratio != 0 else 0
    b_log_b = b_ratio * math.log10(b_ratio) if b_ratio != 0 else 0

    # Finally, calculate the entropy.....
    entropy = (-1) * (a_log_a + b_log_b)
    return entropy


# Print result in the console
def console_log(data, indent=0):
    # Treat "Name" tage specially
    condition_name = data.get("Name")
    if condition_name is not None:
        print("\n\n>>>>>>>>>>>> " + condition_name + " <<<<<<<<<<<<")
        del data['Name']

    # Traverse all the data items.
    for key, val in data.items():
        # Dictionary type, parse section
        if isinstance(val, dict):
            # Trick: make header constant length
            left_hyphens = (31 - len(key)) // 2
            right_hyphens = 31 - len(key) - left_hyphens
            title = "|-" + "-" * left_hyphens + key + "-" * right_hyphens + "-|"

            # Section title
            print(title)
            console_log(val, indent+1)
        else:
            # Section contents
            print(key + ": " + str(val))


# Count positive and negative samples within a conditional class
def count_within_condition(cond_class, target):
    sample_neg = 0
    sample_pos = 0
    for target_index in cond_class:
        if target[target_index] == 0:
            sample_neg += 1
        elif target[target_index] == 1:
            sample_pos += 1
    return sample_neg, sample_pos


# Input binary condition and binary target, output information gain
def binary_analysis(condition, target, cond_name="Binary Analysis"):

    # Categorize into 2 conditions: negative and positive
    id_cond_neg = []       # index of negative conditions
    id_cond_pos = []       # index of positive conditions

    for index, row in enumerate(condition):
        if row == 0:
            id_cond_neg.append(index)
        elif row == 1:
            id_cond_pos.append(index)
        else:
            raise ValueError("Invalid binary value!")

    # Negative and positive part for each conditions
    [num_neg_neg, num_neg_pos] = count_within_condition(id_cond_neg, target)
    [num_pos_neg, num_pos_pos] = count_within_condition(id_cond_pos, target)

    # Compute entropy
    # Compute number of target neg & pos
    num_targ_neg = 0
    num_targ_pos = 0
    for target_value in target:
        if target_value == 0:
            num_targ_neg += 1
        else:
            num_targ_pos += 1

    # Parent entropy
    num_total = num_targ_neg + num_targ_pos       # Total num of records
    e_parent = get_entropy(num_targ_neg, num_targ_pos)

    # Child entropy
    # Number of instances in each condition
    num_cond_neg = len(id_cond_neg)
    num_cond_pos = len(id_cond_pos)

    # Weights of each condition
    cond_neg_ratio = num_cond_neg / num_total if num_total != 0 else 0      # Target negative
    cond_pos_ratio = num_cond_pos / num_total if num_total != 0 else 0      # Target positive

    # Entropy of each condition
    e_neg = get_entropy(num_neg_neg, num_neg_pos)       # Condition negative
    e_pos = get_entropy(num_pos_neg, num_pos_pos)       # Condition positive

    # Information gain
    info_gain = e_parent - (
            cond_neg_ratio * e_neg +
            cond_pos_ratio * e_pos
    )

    # Print in console
    data = {
        "Name": cond_name,
        "Records": {
            "Num of negative condition": num_cond_neg,
            "Num of positive condition": num_cond_pos,
            "Num of negative target": num_targ_neg,
            "Num of positive target": num_targ_pos,
            "Negative ratio": cond_neg_ratio,
            "Positive ratio": cond_pos_ratio,
            "Total record num": num_total,
        },
        "Entropy": {
            "Parent Entropy": e_parent,
            "Condition negative entropy": e_neg,
            "Condition positive entropy": e_pos,
        },
        "Information Gain": {
            "Info gain": info_gain,
        }
    }
    console_log(data)
    return info_gain


# Input numeric condition and binary target, output information gain
def numeric_analysis(condition, target, cond_name="Numeric Analysis"):
    # Defines left mean and right mean
    mean_val = condition.mean()
    left_mean = (condition.min() + mean_val) / 2
    right_mean = (condition.max() + mean_val) / 2

    # Categorize into 3 conditions: small, medium, and large
    id_cond_small = []          # condition small
    id_cond_medium = []         # condition medium
    id_cond_large = []          # condition large

    for index, row in enumerate(condition):
        if row < left_mean:
            id_cond_small.append(index)
        elif row > right_mean:
            id_cond_large.append(index)
        else:
            id_cond_medium.append(index)

    # Negative and positive part of each conditions
    [s_neg, s_pos] = count_within_condition(id_cond_small, target)
    [m_neg, m_pos] = count_within_condition(id_cond_medium, target)
    [l_neg, l_pos] = count_within_condition(id_cond_large, target)

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
    # Number of instances in each condition
    num_cond_small = len(id_cond_small)
    num_cond_medium = len(id_cond_medium)
    num_cond_large = len(id_cond_large)

    # Weights of each condition
    cond_small_ratio = num_cond_small / num_total if num_total != 0 else 0
    cond_medium_ratio = num_cond_medium / num_total if num_total != 0 else 0
    cond_large_ratio = num_cond_large / num_total if num_total != 0 else 0

    # Entropy of each condition
    e_small = get_entropy(s_neg, s_pos)
    e_medium = get_entropy(m_neg, m_pos)
    e_large = get_entropy(l_neg, l_pos)

    # Information gain
    info_gain = e_parent - (
            cond_small_ratio * e_small +
            cond_medium_ratio * e_medium +
            cond_large_ratio * e_large
    )

    # Print result
    data = {
        "Name": cond_name,
        "Records": {
            "Num of condition small": num_cond_small,
            "Num of condition medium": num_cond_medium,
            "Num of condition large": num_cond_large,
            "Num of negative target": num_targ_neg,
            "Num of positive target": num_targ_pos,
            "Num of small ratio": cond_small_ratio,
            "Num of medium ratio": cond_medium_ratio,
            "Num of large ratio": cond_large_ratio,
            "Total record num": num_total,
        },
        "Entropy": {
            "Parent entropy": e_parent,
            "Entropy small": e_small,
            "Entropy medium": e_medium,
            "Entropy large": e_large
        },
        "Information Gain": {
            "Info gain": info_gain,
        }
    }
    console_log(data)

    return info_gain


# Hybrid analysis, combining numeric and binary analysis.
def hybrid_analysis(condition, target, is_binary=True, name="Analysis Name"):
    if is_binary:
        info_gain = binary_analysis(condition, target, name)
    else:
        info_gain = numeric_analysis(condition, target, name)
    return info_gain

# ------------------------- Evaluation Part ---------------------------

# Read Excel file and do analysis
file_path = './movie_list/movie_data.xlsx'
movie_data = pd.read_excel(file_path)
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
print("\n\n~~~~~~~~~~~ Info Gain Ranking ~~~~~~~~~~~")
for i, (name, value) in enumerate(variables_sorted):
    print(f"{i+1}. Info Gain from {name}: {value}")





