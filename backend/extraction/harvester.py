# @Author: shounak
# @Date:   2022-02-19T15:52:24-08:00
# @Email:  shounak@stanford.edu
# @Filename: harvester.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-20T00:30:59-08:00

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
TIMEOUT = 20
SEED_TIMEOUT = TIMEOUT + 10
SIMILARTY_THRESH = 0.7
stop_words = set(stopwords.words('english'))

# API_KEY = "AIzaSyBVnIpS431p2BOA-R6Pjz9gAprjg0A4Jp8"
API_KEY = "AIzaSyAr4eiB6oqClTREPpU0okBzwUnfF53XiOA"
CSE_ID = "fc0451f6e29dca5d4"
TOTAL_SENTIMENTS = []

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
        raise KeyError("Couldn't find seed meta data")
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

def configure_nx(meta_data: dict,
                 percentile = None,
                 top_n: int = None,
                 hits: int = 2,
                 include_self_loops: bool = False,
                 include_isolates: bool = False,
                 normalize_weights: bool = True,
                 net_behaviour: bool = False,
                 compress_edgedata: bool = True,
                 weight_str: str = 'value',
                 format: str = 'dataframe',
                 draw: bool = False) -> [(pd.core.frame.DataFrame, pd.core.frame.DataFrame,
                                          pd.core.frame.DataFrame, pd.core.frame.DataFrame,
                                          pd.core.frame.DataFrame),
                                         (nx.DiGraph, dict, list)]:
    """Short summary.
    Parameters
    ----------
    meta_data : dict
        A dictionary with the node sizes and edges of the graph at hand.
    percentile : Optional[float]
        NOTE: Not recommended. Outliers in edge weights undermine the functionality of this feature.
        The top `percentile`-th data is kept to reduce graph complexity.
    top_n : Optional[int]
        NOTE: This is recommended over `percentile` and `hits`.
        The `top_n` edges to retain in the graph.
    hits : Optional[int]
        NOTE: Not recommended by extension: related to `percentile`.
        The top `percentile`-th data is filtered, and again `hits` times to reduce graph complexity.
    include_self_loops : bool
        Whether self-loops should be includes in the final graph.
    include_isolates : bool
        Whether isolates (a node without any incoming/outgoing edges) should be included in the final graph.
    normalize_weights : bool
        NOTE: Many packages may perform this normalization as part of their core JavaScript functionality.
        Whether node sizes should be normalized.
    net_behaviour : bool
        Whether only summed edge vector should be calculated and considered in the final graph.
    compress_edgedata : bool
        NOTE: Should always be `False` for DeepSea, and only be `True` for vis.js rendering.
        Whether edge data should be compressed in mutated `meta_data`.
    weight_str : str
        The name of the weight string for VIS.JS purposes.
    format : str
        NOTE: Should always be dataframe for DeepSea, and only be "raw" for vis.js rendering.
        Either "dataframe" or "raw".
    draw : bool
        NOTE: This is only for local validation purposes, no impact on DeepSea output.
              Causes additional run-time processing due to local matplotlib figure generation.
        Quick and dirty rendering. Whether the Python-generated networkx graph should be outputted to the console.
    Returns
    -------
    [(pd.core.frame.DataFrame, pd.core.frame.DataFrame,
                                         pd.core.frame.DataFrame, pd.core.frame.DataFrame,
                                         pd.core.frame.DataFrame),
                                        (nx.DiGraph, dict, list)]
        If `format` := "dataframe", then five dataframes corresponding to the nodes, node sizes,
        edges, loners, and self-loops are returned.
        If `format` := "raw", then the networkx graph, the meta data, and a list of considered parameters
        are returned.
    """
    _print('Configuring NX Object...')

    # Just for local testing.
    considered_filters = {k: v for k, v in locals().copy().items() if not isinstance(v, pd.core.frame.DataFrame)}

    def remove_dupl_edges(G_func: [nx.Graph, nx.DiGraph]) -> [nx.Graph, nx.DiGraph]:
        """Removes any duplicated edges in (u, v, w)/weighted networkx Graph. Not supposed to be here.
        Parameters
        ----------
        G_func : [nx.Graph, nx.DiGraph]
            The original networkx Graph.
        Returns
        -------
        [nx.Graph, nx.DiGraph]
            The fixed networkx Graph.
        """
        # REMOVE DUPLICATE EDGES
        stripped_list = list(set([tuple(set(edge)) for edge in G_func.edges()]))
        stripped_list = [(u, v, d) for u, v, d in G_func.edges(data=True) if (u, v) in stripped_list]
        G_func.remove_edges_from([e for e in G.edges()])
        G_func.add_edges_from(stripped_list)

        return G_func

    # def reject_outliers(data, m=2):
    #     return data[abs(data - np.mean(data)) < m * np.std(data)]

    # Get the data
    edges, node_sizes = meta_data['edges'], meta_data['node_sizes']

    # Normalizing node sizes
    node_sizes = {k: v / max(node_sizes.values()) for k, v in node_sizes.items()} if normalize_weights else node_sizes

    # Formatting node sizes
    node_sizes = {k: {'size': v} for k, v in node_sizes.items()}

    # Selectively show edges based on percentile, if speciified
    G = nx.DiGraph()
    G.add_weighted_edges_from(edges, weight_str)
    if percentile is not None:
        percentile = float(percentile)

        weights_all = list([d[weight_str] for u, v, d in G.edges(data=True)])
        cutoff = np.percentile([c for c in weights_all if c > 0], percentile)
        _print('STATUS: Cuttoff is: ' + str(cutoff) + ' @ {} percentile'.format(percentile))
        G_filt = nx.DiGraph()
        G_filt.add_weighted_edges_from([(u, v, d) for u, v, d in G.edges(data=True) if d[weight_str] > cutoff],
                                       weight_str)
        G = G_filt.copy()
    elif top_n is not None:
        frequency_dict = {k: v[weight_str] for k, v in Counter(G.edges).items()}
        # TEMP: Temporarily not removing any maximas or minimas, taken care by normalization
        # # Removing some extremas
        # for i in range(hits):
        #     frequency = list(reject_outliers(np.array(list(frequency_dict.values())), m=1))
        #     frequency_dict = {k: v for k, v in frequency_dict.items() if v in frequency}

        frequency_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True))
        frequency_dict = dict(list(frequency_dict.items())[:top_n])

        # Add edges
        G_filt = nx.DiGraph()
        G_filt.add_weighted_edges_from([(*k, v) for k, v in frequency_dict.items()], weight_str)
        G = G_filt.copy()

    # TEMP: Right now, node colors are 1:1 with the nodes themselves, not based on another hierarchy
    nx.set_node_attributes(G, dict(zip(G.nodes, G.nodes)), 'group')

    # Removing duplicate edges if specified
    G = remove_dupl_edges(G) if net_behaviour else G

    # Calculating extra attributes
    selfloops = list(nx.selfloop_edges(G, data=True))
    _print(f'> Self-loops: {selfloops}')
    meta_data['node_sizes'] = {node: size for node, size in meta_data['node_sizes'].items() if node in G.nodes}

    # Remove from networkx graph if specified
    G.remove_edges_from([(a, b) for a, b, c in selfloops]) if not include_self_loops else None
    loners = list(nx.isolates(G))
    _print(f'> Isolates: {loners}')
    G.remove_edges_from(loners) if not include_isolates else None

    if draw:
        plt.figure(figsize=(10, 10))
        nx.draw(G, nx.kamada_kawai_layout(G), with_labels=True)

    # Add information to meta data
    if format == 'raw':
        meta_data['loners'] = loners
        meta_data['selfloops'] = selfloops
        edges = [(a, b, c[weight_str]) for a, b, c, in list(G.edges(data=True))
                 ] if compress_edgedata else list(G.edges(data=True))
        meta_data['edges'] = edges
        meta_data['nodes'] = list(G.nodes)
        return G, meta_data, considered_filters
    else:
        meta_data['loners'] = pd.DataFrame(loners, columns=['loners'])
        meta_data['selfloops'] = pd.DataFrame([(a, b, c[weight_str]) for a, b, c in selfloops],
                                              columns=['from', 'to', 'weight'])
        edges = [(a, b, c[weight_str]) for a, b, c, in list(G.edges(data=True))]
        meta_data['edges'] = pd.DataFrame(edges, columns=['from', 'to', 'weight'])
        meta_data['nodes'] = pd.DataFrame(list(G.nodes), columns=['node'])
        meta_data['node_sizes'] = pd.DataFrame(meta_data['node_sizes'],
                                               index=[0]).T.reset_index().rename(columns={'index': 'node',
                                                                                          0: 'node_size'})
        return (meta_data['nodes'], meta_data['node_sizes'], meta_data['edges'],
                meta_data['loners'], meta_data['selfloops'])


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

search_queries = get_queries(SEED_URL)

urls_accessed = []
titles_accessed = []
node_content = {}

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
        title = res['title']
        _print(f"> Result Scan: {link}", 'WHITE')

        # If the candidate article is not historically_similar, find meta data
        # and add to graph
        if not historically_similar(titles_accessed, title):
            # Get Meta Data
            child_meta_data = safe_meta_search(link)
            if child_meta_data is not None:
                titles_accessed.append(title)
                urls_accessed.append(link)
                node_content[link] = child_meta_data

def format_as_dataframe(node_content):
    # to/from/weights
    nodes_relation: dict = {str(i): list(node_content.keys())[i] for i in range(len(node_content))}
    all_contents = [d['content'] for d in node_content.values()]
    out = determine_similarity_tfidf(list(all_contents))
    df = pd.DataFrame(out, columns=nodes_relation)
    df.values[[np.arange(len(df))]*2] = np.nan
    df = df.stack().reset_index()
    df.columns = ['to', 'from', 'weight']
    df['weight'] = df['weight'].round(4)

    # node attributes

    return df

df = format_as_dataframe(node_content)

def convert_to_graph():
    # Source, target
    G = nx.from_pandas_edgelist(df, 'to', 'from', ['weight'])

    # JSON file


nx.draw(G)
layout = nx.spring_layout(G)
fig = plt.figure(figsize=(12, 8))
nx.draw(G, layout)
_ = nx.draw_networkx_edge_labels(G, pos=layout)
plt.show()

plt.hist(TOTAL_SENTIMENTS, bins=20)

# EOF
