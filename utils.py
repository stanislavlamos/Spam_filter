import re
import math

# a list of keywords that have nothing to do with email spam/ham status
HEADER_NAMES_LIST = ["return-path", "delivery-date", "received", "message-id", "mon", "tue", "wed", "thu", "fri", "sat",
                     "sun", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "from",
                     "subject", "id", "to", "date", "content-type", "x-keywords", "by", "x-info", "body", "errors-to",
                     "x-mailman-version"]

NON_WORD_CHARACTERS = ".,:;-!=*/()"

SPAM_TAG = "SPAM"
HAM_TAG = "OK"


# Read classification of emails from !truth.txt
def read_classification_from_file(filename):
    dict_out = {}
    with open(filename, 'rt', encoding='utf-8') as f:
        for line in f:
            line_list = line.split()
            dict_out[line_list[0]] = line_list[1]

    return dict_out


# Write our prediction to !prediction.txt
def write_classification_to_file(path, classification):
    with open(f"{path}/!prediction.txt", 'w', encoding='utf-8') as f:
        filenames = list(classification.keys())
        classifications = list(classification.values())
        for i in range(len(filenames)):
            f.write(f"{filenames[i]} {classifications[i]}\n")


# Remove html tags from string
def remove_html_tags(text):
    tag_re = re.compile(r'<[^>]+>')

    return tag_re.sub('', text)


# Get general probabilities of a message being spam or ham based on training data
def get_prior_probabilities(filename):
    classification = read_classification_from_file(filename)
    spam_count = 0
    ham_count = 0
    for filename in classification.keys():
        if classification[filename] == SPAM_TAG:
            spam_count += 1
        elif classification[filename] == HAM_TAG:
            ham_count += 1

    ham_probability = ham_count / (spam_count + ham_count)
    spam_probability = spam_count / (spam_count + ham_count)

    return spam_probability, ham_probability


# Classify string as a word a strip non word characters
def classify_string(word):
    word = word.strip(NON_WORD_CHARACTERS).lower()
    if len(word) == 0 or word[0].isdigit():
        return None

    return word


# Get all words in an email and return them as a dictionary in format {word : count}
def get_email_vocabulary(body, vocabulary):
    body_string = remove_html_tags(body)
    body_list = body_string.split()
    for word in body_list:
        word = classify_string(word)
        if word is not None:
            vocabulary[word] = vocabulary.get(word, 0) + 1

    return vocabulary


# Increment values of every key by one
# This is used for spam and ham vocabularies to avoid probability value 0
def increment_value_of_keys_by_1(vocabulary, all_words):
    for word in all_words:

        if word in vocabulary:
            vocabulary[word] += 1
            continue

        vocabulary[word] = vocabulary.get(word, 1)

    return vocabulary


# Update a vocabulary during it's generation on a dataset
def update_vocabulary(body, vocabulary):
    body_string = remove_html_tags(body)
    body_list = body_string.split()
    for word in body_list:
        word = classify_string(word)
        if word is not None:
            vocabulary[word] = vocabulary.get(word, 0) + 1

    return vocabulary


# Generate a dictionary of all words in a dataset and their count in format {word : count}
def generate_vocabulary(corpus):
    vocabulary = {}
    for filename, body in corpus:
        vocabulary = update_vocabulary(body, vocabulary)

    return vocabulary


# Calculate probability of each word being in a given dataset and return as dictionary
def calculate_probability_for_words(vocabulary):
    probability_dict = {}
    zero_counter = 0
    total_number_of_words = sum(vocabulary.values())
    for word in vocabulary.keys():
        probability = vocabulary[word] / total_number_of_words
        probability_dict[word] = probability

    return probability_dict


# Deconstruct email body and return as list of words
def deconstruct_email(email_body):
    body_string = remove_html_tags(email_body)
    body_list = (body_string.split())
    for word in body_list:
        word = word.strip(NON_WORD_CHARACTERS).casefold()

    return body_list


# Classifying an email and returning the probability of being spam or ham
def classify_email(email_body, probability_dict, prior_probability):
    body_list = deconstruct_email(email_body)
    res = 0

    for word in body_list:
        if word in probability_dict.keys():
            res += math.log(probability_dict[word])

    res += math.log(prior_probability)

    return res
