# @Author: shounak
# @Date:   2022-02-19T00:51:04-08:00
# @Email:  shounak@stanford.edu
# @Filename: local_nlp.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T02:03:19-08:00


import os
from backend.scraping_defs import get_content
from backend.util import download_nltk_dependecy
import nltk
from nltk.corpus import stopwords
download_nltk_dependecy('stopwords')
download_nltk_dependecy('punkt')
download_nltk_dependecy('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from typing import Final
import string
from collections import Counter
import numpy as np

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

TEST_URL: Final = "https://www.reuters.com/world/europe/shelling-breaks-out-east-ukraine-west-moscow-dispute-troop-moves-2022-02-17/"
useless_chars: tuple = tuple(string.punctuation)

_ = """
####################################################################################################
############################################ DEFINITIONS ###########################################
#################################################################################################"""

def get_clean_words(content: str, remove_puncs: bool = True, uniq: bool = True) -> list:
    tokens = word_tokenize(content, language='english')
    no_stopw = [word for word in tokens if not word in stopwords.words()]

    if remove_puncs:
        no_stopw = [s for s in no_stopw if (s not in useless_chars) and
                                           (not s.startswith(useless_chars))]

    return no_stopw if not uniq else list(set(no_stopw))

def get_sentences(content: str) -> list:
    return content.split('\n')

def kw_frequency(word_list: list) -> dict:
    return dict(Counter(word_list).most_common())

def get_top_words(freq_list: dict, percentile: Final = 60) -> dict:
    freq_thresh = np.percentile(list(set(kw_freq.values())), 60)
    return {k: v for k, v in freq_list.items() if v > freq_thresh}

content = get_content(TEST_URL)
all_clean_words = get_clean_words(content, uniq = False)
kw_freq = kw_frequency(clean_words)
top_words = get_top_words(kw_freq)
uniq_clean_words = get_clean_words(content, uniq = True)
word_pos = dict(nltk.pos_tag(uniq_clean_words))

# EOF
