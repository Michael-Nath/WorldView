# @Author: shounak, michael
# @Date:   2022-02-19T00:51:04-08:00
# @Email:  shounak@stanford.edu, mnath@stanford.edu
# @Filename: local_nlp.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-20T00:27:42-08:00


def _set_cwd():
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
_set_cwd()

from re import sub
from nltk import collocations, pos_tag, corpus, word_tokenize
from heapq import nlargest
from nltk.corpus import stopwords
from util import download_nltk_dependecy, _print
_DEPS = ('stopwords', 'punkt', 'averaged_perceptron_tagger', 'vader_lexicon', 'wordnet')
for d in _DEPS:
    download_nltk_dependecy(d)
from nltk.tokenize import word_tokenize
import string
from collections import Counter
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

_print(f"{__file__}: DEPENDENCIES INSTALLED", 'LIGHTBLUE_EX')

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

# def get_pos_tags(word_list: list) -> dict:
#     output = dict(pos_tag(word_list))
#     return output

def get_sentiment(text_selection) -> dict:
    sia = SentimentIntensityAnalyzer()
    return sia.polarity_scores(text_selection)

def get_top_phrases(word_list: list, LIMIT: int = 100, THRESH: int = 1) -> dict:
    finder = collocations.TrigramCollocationFinder.from_words(word_list)
    filt = dict([e for e in finder.ngram_fd.most_common(LIMIT) if e[1] > THRESH])
    return  {', '.join(k): v for k, v in filt.items()}

def summarize_content(content: str) -> list:
    # get sentences
    formatted_content = sub('[^a-zA-Z]', ' ', content )
    sentences = get_sentences(content)
    formatted_content = sub(r'\s+', ' ', formatted_content)
    stop_words = corpus.stopwords.words('english')
    word_frequencies = {}
    for word in word_tokenize(formatted_content):
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    sentence_scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    return "\n".join(summary_sentences)


def _ANALYZE_META_DATA(URL_META_DATA: dict) -> dict:
    _content = URL_META_DATA['content']
    _headline = URL_META_DATA['headline']

    content_sentiment = get_sentiment(_content)
    content_summary = summarize_content(_content)
    headline_sentiment = get_sentiment(_headline)
    all_clean_words = get_clean_words(_content, uniq = False)
    kw_freq = kw_frequency(all_clean_words)
    top_words = get_top_words(_content)
    top_phrases = get_top_phrases(all_clean_words)
    # uniq_clean_words = list(set(all_clean_words))
    # pos_tags = get_pos_tags(uniq_clean_words)

    JSON_OBJECT = {'content_sentiment': content_sentiment,
                   'content_summary': content_summary,
                   'headline_sentiment': headline_sentiment,
                   # 'clean_words': all_clean_words,
                   'keyword_frequency': kw_freq,
                   'top_words': top_words,
                   'top_phrases': top_phrases}
                   # 'unique_words': uniq_clean_words}
                   # 'parts_of_speech': pos_tags}

    URL_META_DATA.update(JSON_OBJECT)

    return URL_META_DATA

# EOF
