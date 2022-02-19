# @Author: shounak
# @Date:   2022-02-19T00:51:04-08:00
# @Email:  shounak@stanford.edu
# @Filename: local_nlp.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T15:41:45-08:00


def _set_cwd():
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
_set_cwd()

import nltk
from nltk.corpus import stopwords
from util import download_nltk_dependecy
_DEPS = ('stopwords', 'punkt', 'averaged_perceptron_tagger', 'vader_lexicon', 'wordnet')
for d in _DEPS:
    download_nltk_dependecy(d)
from nltk.tokenize import word_tokenize
import string
from collections import Counter
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

print(f"{__file__}: DEPENDENCIES INSTALLED")

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

PUNC_CHARS: tuple = tuple(string.punctuation)

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

def get_top_words(selection: str) -> dict:
    doc = nlp(selection)
    entities = [{'word': X.text, 'type': X.label_} for X in doc.ents]
    num_tags = [f"entity_{i+1}" for i in range(len(doc.ents))]
    return dict(zip(num_tags, entities))

def get_pos_tags(word_list: list) -> dict:
    output = dict(nltk.pos_tag(word_list))
    return output

def get_sentiment(text_selection) -> dict:
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text_selection)

def get_top_phrases(word_list: list, LIMIT: int = 100, THRESH: int = 1) -> dict:
    finder = nltk.collocations.TrigramCollocationFinder.from_words(word_list)
    filt = dict([e for e in finder.ngram_fd.most_common(LIMIT) if e[1] > THRESH])
    key_iter = list(filt.keys())
    return  {f"phrase_{k_i+1}": {', '.join(key_iter[k_i]): filt[key_iter[k_i]]} for k_i in range(len(key_iter))}

def _ANALYZE_META_DATA(URL_META_DATA: dict) -> dict:
    _content = URL_META_DATA['content']
    _headline = URL_META_DATA['headline']

    content_sentiment = get_sentiment(_content)
    headline_sentiment = get_sentiment(_headline)
    all_clean_words = get_clean_words(_content, uniq = False)
    kw_freq = kw_frequency(all_clean_words)
    top_words = get_top_words(_content)
    top_phrases = get_top_phrases(all_clean_words)
    uniq_clean_words = list(set(all_clean_words))
    pos_tags = get_pos_tags(uniq_clean_words)

    JSON_OBJECT = {'content_sentiment': content_sentiment,
                   'headline_sentiment': headline_sentiment,
                   'clean_words': all_clean_words,
                   'keyword_frequency': kw_freq,
                   'top_words': top_words,
                   'top_phrases': top_phrases,
                   'unique_words': uniq_clean_words,
                   'parts_of_speech': pos_tags}

    URL_META_DATA.update(JSON_OBJECT)

    return URL_META_DATA

# EOF
