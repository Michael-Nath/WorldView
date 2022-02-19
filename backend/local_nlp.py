# @Author: shounak
# @Date:   2022-02-19T00:51:04-08:00
# @Email:  shounak@stanford.edu
# @Filename: local_nlp.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T04:03:48-08:00


import os
from backend.scraping_defs import get_content
from backend.util import download_nltk_dependecy
import nltk
from nltk.corpus import stopwords
download_nltk_dependecy('stopwords')
download_nltk_dependecy('punkt')
download_nltk_dependecy('averaged_perceptron_tagger')
download_nltk_dependecy('vader_lexicon')
download_nltk_dependecy('wordnet')
from nltk.tokenize import word_tokenize
from typing import Final
import string
from collections import Counter
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

TEST_URL: Final = "https://www.reuters.com/world/europe/shelling-breaks-out-east-ukraine-west-moscow-dispute-troop-moves-2022-02-17/"
PUNC_CHARS: tuple = tuple(string.punctuation)

# with open('backend/ref/pos_fullform.txt') as f:
#     POS_MAP = dict([l.replace('\n', '').split(' ', 1) for l in f.readlines()])

_ = """
####################################################################################################
############################################ DEFINITIONS ###########################################
#################################################################################################"""

def get_clean_words(content: str, remove_puncs: bool = True, uniq: bool = True) -> list:
    tokens = word_tokenize(content, language='english')
    no_stopw = [word for word in tokens if not word in stopwords.words()]

    if remove_puncs:
        no_stopw = [s for s in no_stopw if (s not in PUNC_CHARS) and
                                           (not s.startswith(PUNC_CHARS))]

    return no_stopw if not uniq else list(set(no_stopw))

def get_sentences(content: str) -> list:
    return content.split('\n')

def kw_frequency(word_list: list) -> dict:
    return dict(Counter(word_list).most_common())

def get_top_words(freq_list: dict, percentile: Final = 60) -> dict:
    freq_thresh = np.percentile(list(set(kw_freq.values())), 60)
    return {k: v for k, v in freq_list.items() if v > freq_thresh}

def get_pos_tags(word_list: list) -> dict:
    output = dict(nltk.pos_tag(word_list))
    return output

def get_sentiment(text_selection):
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text_selection)

def get_top_phrases(word_list: list, LIMIT: int = 100, THRESH: int = 1):
    finder = nltk.collocations.TrigramCollocationFinder.from_words(word_list)
    return dict([e for e in finder.ngram_fd.most_common(LIMIT) if e[1] > THRESH])


def analyze_master(TEST_URL):
    URL_META_DATA: Final = get_content(TEST_URL)
    content = URL_META_DATA['content']
    headline = URL_META_DATA['headline']
    author = URL_META_DATA['author']
    all_clean_words = get_clean_words(content, uniq = False)
    kw_freq = kw_frequency(all_clean_words)
    top_words = get_top_words(kw_freq)
    uniq_clean_words = list(set(all_clean_words))
    pos_tags = get_pos_tags(list(set(uniq_clean_words)))
    top_phrases = get_top_phrases(all_clean_words)

    JSON_OBJECT = {'URL': TEST_URL,
                   'content': content,
                   'headline': headline,
                   'author': author,
                   'clean_words': all_clean_words,
                   'keyword_frequency': kw_freq,
                   'top_words': top_words,
                   'top_phrases': top_phrases,
                   'unique_words': uniq_clean_words,
                   'parts_of_speech': pos_tags}

# EOF
