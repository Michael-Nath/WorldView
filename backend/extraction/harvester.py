# @Author: shounak
# @Date:   2022-02-19T15:52:24-08:00
# @Email:  shounak@stanford.edu
# @Filename: harvester.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T21:21:05-08:00

# def _set_cwd():
#     import os
#     abspath = os.path.abspath(__file__)
#     dname = os.path.dirname(abspath)
#     os.chdir(dname)
# _set_cwd()

from backend.extraction.core_extraction import CORE_EXECUTION
from backend.extraction.util import (safe_request, valid_getreq,
                                     time_limit, TimeoutException)
# import extraction.core_extraction as SINGLE_EXTRACTION
# from extraction.util import safe_request, check_validity
import numpy as np
# import search_engines
import requests
from googleapiclient.discovery import build
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import networkx as nx

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""
# STD_THRESH = 0.3
SEED_URL = "https://www.cnn.com/2022/02/19/health/fourth-covid-19-vaccine-dose-us/index.html"
SEARCH_FORWARD = 5
TOP_N = 2
TIMEOUT = 10
SEED_TIMEOUT = TIMEOUT + 10
SIMILARTY_THRESH = 0.7

# API_KEY = "AIzaSyBVnIpS431p2BOA-R6Pjz9gAprjg0A4Jp8"
API_KEY = "AIzaSyAr4eiB6oqClTREPpU0okBzwUnfF53XiOA"
CSE_ID = "fc0451f6e29dca5d4"
TOTAL_SENTIMENTS = []

_ = """
####################################################################################################
############################################ DEFINITIONS ###########################################
#################################################################################################"""

def similar(str_a, str_b):
    return SequenceMatcher(None, str_a, str_b).ratio()

# May be used to compare similarity of one article to an entire cluster
def historically_similar(all_so_far: str, curl: str):
    for url in all_so_far:
        similarity_score = similar(url, curl)
        TOTAL_SENTIMENTS.append(similarity_score)
        if similarity_score > SIMILARTY_THRESH:
            print(f">>> Current title: {curl} is similar to {url}")
            return True
        print(f">>> OK similarity: {similarity_score}")
    return False

def safe_meta_search(URL, TIMEOUT=TIMEOUT):
    def graceful_search(URL):
        META_DATA = None
        try:
            META_DATA = CORE_EXECUTION(URL)
        except:
            pass
        return META_DATA

    try:
        with time_limit(TIMEOUT):
            meta_data = graceful_search(URL)
    except TimeoutException:
        pass

    return meta_data

def get_queries(SEED_URL, TOP_N=TOP_N):
    SEED_META_DATA = safe_meta_search(SEED_URL, TIMEOUT=SEED_TIMEOUT)
    if SEED_META_DATA is None:
        raise KeyError("Couldn't find seed meta data")
    search_queries = list(SEED_META_DATA['top_phrases'].keys())[:TOP_N]
    return search_queries

def google_search(search_term, my_api_key=API_KEY, my_cse_id=CSE_ID, **kwargs):
    service = build("customsearch", "v1", developerKey=my_api_key)
    try:
        res = service.cse().list(q=search_term, cx=my_cse_id, **kwargs).execute()
        return res['items']
    except e:
        print(f">> Could not complete search, skipping.\n{e}")
        return {}

_ = """
####################################################################################################
############################################ DEFINITIONS ###########################################
#################################################################################################"""

def determine_similarity_tfidf(documents):
    tokenizer=LemmaTokenizer()
    token_stop = tokenizer(' ’.join(stop_words))
    vectorizer = TfidfVectorizer(stop_words=token_stop, tokenizer=tokenizer)
    doc_vectors = vectorizer.fit_transform(documents)
    cosine_similarities = linear_kernel(doc_vectors, doc_vectors)

search_queries = get_queries(SEED_URL)

urls_accessed = []
titles_accessed = []

edge_list = []
node_list = []
for query in search_queries:
    print(f"CHILD: {query}")
    # Search google for similar articles
    results = google_search(query, num=SEARCH_FORWARD)
    if (results == {}):
        continue

    # Get meta data for each link for inputted keywords
    for res in results:
        link = res['link']
        title = res['title']
        print(f"> Result Scan: {link}")
        # If the candidate article is not historically_similar, find meta data
        # and add to graph
        if not historically_similar(titles_accessed, title):
            titles_accessed.append(title)
            urls_accessed.append(link)
            # Get Meta Data
            child_meta_data = safe_meta_search(link)
            if child_meta_data is None:
                pass
            else:
                # TODO: Contribute to graph
                pass

plt.hist(TOTAL_SENTIMENTS, bins=20)

# EOF
