# @Author: shounak
# @Date:   2022-02-19T15:52:24-08:00
# @Email:  shounak@stanford.edu
# @Filename: harvester.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-20T04:26:17-08:00

# def _set_cwd():
#     import os
#     abspath = os.path.abspath(__file__)
#     dname = os.path.dirname(abspath)
#     os.chdir(dname)
# _set_cwd()

from backend.extraction.core_extraction import CORE_EXECUTION
from backend.extraction.util import (safe_request, valid_getreq,
                                     time_limit, TimeoutException, _print,
                                     download_nltk_dependecy)
# import extraction.core_extraction as SINGLE_EXTRACTION
# from extraction.util import safe_request, check_validity
import numpy as np
# import search_engines
import requests
from googleapiclient.discovery import build
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
download_nltk_dependecy('omw-1.4')
download_nltk_dependecy('punkt')
from nltk.corpus import stopwords

__file__ = 'harverster.py'

_print(f"{__file__}: DEPENDENCIES INSTALLED", 'LIGHTBLUE_EX')

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""
# STD_THRESH = 0.3
SEED_URL = "https://www.cnn.com/2022/02/19/health/fourth-covid-19-vaccine-dose-us/index.html"
SEARCH_FORWARD = 5
TOP_N = 2
stop_words = set(stopwords.words('english'))

# API_KEY = "AIzaSyBVnIpS431p2BOA-R6Pjz9gAprjg0A4Jp8"
API_KEY = "AIzaSyAr4eiB6oqClTREPpU0okBzwUnfF53XiOA"
CSE_ID = "fc0451f6e29dca5d4"
TOTAL_SENTIMENTS = []

# Harvesting
depth = 0
MAX_DEPTH = 2
TIMEOUT = 20
SEED_TIMEOUT = TIMEOUT + 10
SIMILARTY_THRESH = 0.7

class LemmaTokenizer:
    ignore_tokens = (',', '.', ';', ':', '"', '``', "''", '`')
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc) if t not in self.ignore_tokens]

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
            _print(f">>> [{similarity_score}] Current title: {curl} is similar to {url}", 'YELLOW')
            return True
        # _print(f">>> OK similarity: {similarity_score}")
    return False

def safe_meta_search(URL, TIMEOUT=TIMEOUT):
    def graceful_search(URL):
        META_DATA = None
        try:
            META_DATA = CORE_EXECUTION(URL)
        except Exception as e:
            _print("[NON-FATAL] Couldn't open the website. Moving on...", 'LIGHTRED_EX')
            _print(f"Exception: {e}", 'RED')
            pass
        return META_DATA

    try:
        with time_limit(TIMEOUT):
            meta_data = graceful_search(URL)
    except TimeoutException as e:
        _print("[NON-FATAL] Timed out! Moving on...", 'LIGHTRED_EX')
        _print(f"Exception: {e}", 'RED')
        pass

    return meta_data

def get_queries(SEED_URL, TOP_N=TOP_N):
    SEED_META_DATA = safe_meta_search(SEED_URL, TIMEOUT=SEED_TIMEOUT)
    if SEED_META_DATA is None:
        _print("Couldn't find seed meta data", 'LIGHTRED_EX')
        # raise KeyError("Couldn't find seed meta data")
    search_queries = list(SEED_META_DATA['top_phrases'].keys())[:TOP_N]
    return search_queries

def google_search(search_term, my_api_key=API_KEY, my_cse_id=CSE_ID, **kwargs):
    service = build("customsearch", "v1", developerKey=my_api_key)
    try:
        res = service.cse().list(q=search_term, cx=my_cse_id, **kwargs).execute()
        return res['items']
    except Exception as e:
        _print(f">> Could not complete search, skipping.", 'LIGHTRED_EX')
        _print(f"Exception: {e}", 'RED')
        return {}

def norm_base(some_data, out_of_scope=False, up_scalar=1):
    def is_a_number(thing):
        return str(thing).replace('.', '').isdigit()
    def get_xy_bounds(some_data):
        x_max = max([iterable[0] for iterable in some_data])
        x_min = min([iterable[0] for iterable in some_data])
        y_max = max([iterable[1] for iterable in some_data])
        y_min = min([iterable[1] for iterable in some_data])
        return x_max, x_min, y_max, y_min

    def _list_norm(some_data, pre_maxima=None, pre_minima=None,
                   pre_x_max=None, pre_y_max=None, pre_x_min=None, pre_y_min=None, up_scalar=1):
        if len(some_data) <= 1:
            raise ValueError('Iterable must have more than one element!')
        if is_a_number(some_data[0]):
            maxima = max(some_data) if pre_maxima is None else pre_maxima
            minima = min(some_data) if pre_minima is None else pre_minima
            some_data = [(val - minima) / (maxima - minima) for val in some_data]
        elif type(some_data[0]) == list or type(some_data[0]) == tuple:
            # Must be two dimensional
            if len(some_data[0]) > 2:
                raise ValueError('Two-dimension maximum supported only!')
            if pre_x_max is None:
                x_max, x_min, y_max, y_min = get_xy_bounds(some_data)
            else:
                x_max, x_min, y_max, y_min = pre_x_max, pre_x_min, pre_y_max, pre_y_min
            some_data = [(up_scalar * (iterable[0] - x_min) / (x_max - x_min),
                          up_scalar * (iterable[1] - y_min) / (y_max - y_min))
                         for iterable in some_data]
            return some_data

    if type(some_data) == dict:
        first_value = list(some_data.values())[0]
        if (type(first_value[0]) == list or type(first_value[0]) == tuple):  # list of lists
            if(out_of_scope):
                # Consider all coordinates in dictionary when determining bounds
                _converted = list(chain.from_iterable(list(some_data.values())))
                x_max, x_min, y_max, y_min = get_xy_bounds(_converted)
                some_data = {k: _list_norm(v, pre_x_max=x_max, pre_y_max=y_max,
                                           pre_x_min=x_min, pre_y_min=y_min, up_scalar=up_scalar)
                             for k, v in some_data.items()}
            else:
                # Pairwise normalization
                some_data = {k: _list_norm(v, up_scalar=up_scalar) for k, v in some_data.items()}
        else:
            _converted = list(some_data.values())
            _converted = _list_norm(_converted, up_scalar=up_scalar)
            some_data = {k: _converted[list(some_data.keys()).index(k)] for k, v in some_data.items()}
    elif type(some_data) == list or type(some_data) == tuple:
        some_data = _list_norm(some_data, up_scalar=up_scalar)
    else:
        raise TypeError('Data type not supported for normalization!')
    return some_data

def package_information(node_content):
    nodes_relation: dict = {'n-' + str(i): list(node_content.keys())[i]
                            for i in range(len(node_content))}

    def get_edge_list(node_content, nodes_relation):
        all_contents = [d['content'] for d in node_content.values()]
        out = determine_similarity_tfidf(list(all_contents))
        df_edges = pd.DataFrame(out, columns=nodes_relation)
        df_edges.index = ['n-' + str(t) for t in df_edges.index]
        df_edges.values[[np.arange(len(df_edges))]*2] = None
        df_edges = df_edges.stack().reset_index()
        df_edges.columns = ['source', 'target', 'w']
        df_edges['w'] = df_edges['w'].round(4)
        df_edges['source'] = df_edges['source'].astype(str)
        df_edges['target'] = df_edges['target'].astype(str)
        df_edges['w'] = df_edges['w'].astype(np.number)

        edge_list_flattened = list(df_edges.T.to_dict().values())
        i = 0
        for d in edge_list_flattened:
            d['id'] = 'e-' + str(i)
            d['data'] = {'similarity': d['w']}
            del d['w']
            i += 1

        return df_edges, edge_list_flattened

    def get_node_list(node_content, nodes_relation):
        # Node attributes
        rev_nodes_relation = {v: k for k, v in nodes_relation.items()}
        i = 0
        node_attributes = []
        for k, v in node_content.items():
            result = {}
            result['id'] = rev_nodes_relation.get(k)
            result['type'] = 'article'
            result['data'] = v
            i += 1
            node_attributes.append(result)
        return node_attributes

    df_edges, edge_list = get_edge_list(node_content, nodes_relation)
    node_list = get_node_list(node_content, nodes_relation)

    return df_edges, edge_list, node_list

def discover_relevant_articles(SEED_URL, urls_accessed, titles_accessed, node_content,
                               depth=0, MAX_DEPTH=MAX_DEPTH,
                               SEARCH_FORWARD=SEARCH_FORWARD):
    search_queries = get_queries(SEED_URL)
    if search_queries is None:
        return urls_accessed, titles_accessed, node_content
    _print(f"DEPTH: {depth}", 'LIGHTMAGENTA_EX')
    for query in search_queries:
        _print(f"CHILD: {query}", 'LIGHTWHITE_EX')
        # Search google for similar articles
        results = google_search(query, num=SEARCH_FORWARD)
        if (results == {}):
            continue

        # Get meta data for each link for inputted keywords
        for res in results:
            # link = res['link']
            link = res['pagemap']['metatags'][0].get('og:url')
            link = link if link is not None else "COULD NOT FIND FILE"
            # link = sanitize_url(link)
            if link in urls_accessed:
                continue
            title = res['title']
            _print(f"> Result Scan: {link}", 'WHITE')

            # If the candidate article is not historically_similar, find meta data
            # and add to graph
            if not historically_similar(titles_accessed, title):
                # Get Meta Data
                child_meta_data = safe_meta_search(link)
                if child_meta_data is not None:
                    child_meta_data['depth'] = depth
                    titles_accessed.append(title)
                    urls_accessed.append(link)
                    _print("LINK IS BEING ADDED!!!", 'CYAN')
                    node_content[link] = child_meta_data
                    _print(f'\nDEBUG: {len(node_content)} number of entries\n', 'CYAN')
                    if (depth < MAX_DEPTH):
                        (urls_accessed,
                         titles_accessed,
                         node_content) = discover_relevant_articles(
                             SEED_URL = link,
                             urls_accessed = urls_accessed,
                             titles_accessed = titles_accessed,
                             node_content=node_content,
                             depth = depth + 1,
                             MAX_DEPTH = MAX_DEPTH,
                             SEARCH_FORWARD = SEARCH_FORWARD)
    return urls_accessed, titles_accessed, node_content

def convert_to_graph(df_edges):
    G = nx.from_pandas_edgelist(df_edges)
    return G

def get_coordinates(G, layout=nx.kamada_kawai_layout):
    def min_max_norm(vector):
        num = [e - min(vector) for e in vector]
        den = max(vector) - min(vector)
        return num/den

    coord = layout(G)
    x_coordinates = [e[0] for e in list(coord.values())]
    y_coordinates = [e[1] for e in list(coord.values())]
    pairwise = list(zip(x_coordinates, y_coordinates))

    x_norm = [i[0]*100 for i in norm_base(pairwise)]
    y_norm = [i[1]*100 for i in norm_base(pairwise)]
    # plt.scatter(x_coordinates, y_coordinates)
    # plt.scatter(x_norm, y_norm)
    ret = dict(zip(coord.keys(), list(zip(x_norm, y_norm))))
    ret = {k: list((v[0], v[1])) for k, v in ret.items()}
    return ret, coord

_ = """
####################################################################################################
############################################# ANALYTICS ############################################
#################################################################################################"""

def determine_similarity_tfidf(documents):
    tokenizer=LemmaTokenizer()
    token_stop = tokenizer(' '.join(stop_words))
    vectorizer = TfidfVectorizer(stop_words=token_stop, tokenizer=tokenizer)
    doc_vectors = vectorizer.fit_transform(documents)
    cosine_similarities = linear_kernel(doc_vectors, doc_vectors)
    return cosine_similarities

_ = """
####################################################################################################
############################################# EXECUTION ############################################
#################################################################################################"""

""" DON'T TOUCH FROM THIS POINT """

def MASTER_EXECUTION(SEED_URL, depth=0, MAX_DEPTH=MAX_DEPTH, SEARCH_FORWARD=SEARCH_FORWARD):
    urls_accessed = []
    titles_accessed = []
    node_content = {}

    urls_accessed, titles_accessed, node_content = discover_relevant_articles(
        SEED_URL, urls_accessed, titles_accessed, node_content,
        depth=0, MAX_DEPTH=MAX_DEPTH, SEARCH_FORWARD=SEARCH_FORWARD)

    # import json
    # with open('lots_of_meta_data_AGAIN.json', 'w', encoding='utf-8') as f:
    #     json.dump(node_content, f, indent=4, sort_keys=True)

    df_edges, edge_list, node_list = package_information(node_content)

    # TODO: Depth to JSON
    # TODO: People and ORGS and Location as top words

    G = convert_to_graph(df_edges)

    coordinates, nx_layout = get_coordinates(G)

    # Add coordinates to nodelist
    for node in node_list:
        id = node['id']
        node['position'] = coordinates.get(id)

    # fig = plt.figure(figsize=(12, 8))
    # nx.draw(G, nx_layout)
    # _ = nx.draw_networkx_edge_labels(G, pos=nx_layout)
    # plt.show()

    return edge_list, node_list

edge_list, node_list = MASTER_EXECUTION(SEED_URL)

# EOF
