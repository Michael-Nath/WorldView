# @Author: shounak
# @Date:   2022-02-19T15:52:24-08:00
# @Email:  shounak@stanford.edu
# @Filename: harvester.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T19:44:09-08:00

# def _set_cwd():
#     import os
#     abspath = os.path.abspath(__file__)
#     dname = os.path.dirname(abspath)
#     os.chdir(dname)
# _set_cwd()

from backend.extraction.core_extraction import CORE_EXECUTION
from backend.extraction.util import safe_request, valid_getreq
# import extraction.core_extraction as SINGLE_EXTRACTION
# from extraction.util import safe_request, check_validity
import numpy as np
# import search_engines
import requests
from googleapiclient.discovery import build


_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""
# STD_THRESH = 0.3
SEED_URL = "https://www.cnn.com/2022/02/19/health/fourth-covid-19-vaccine-dose-us/index.html"
SEARCH_FORWARD = 5

my_api_key = "AIzaSyBVnIpS431p2BOA-R6Pjz9gAprjg0A4Jp8"
my_cse_id = "fc0451f6e29dca5d4"

_ = """
####################################################################################################
############################################ DEFINITIONS ###########################################
#################################################################################################"""

def safe_meta_search(URL):
    META_DATA = None
    try:
        META_DATA = CORE_EXECUTION(URL)
    except:
        pass
    return META_DATA

def google_search(search_term, my_api_key, my_cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=my_api_key)
    try:
        res = service.cse().list(q=search_term, cx=my_cse_id, **kwargs).execute()
        return res['items']
    except:
        return {}

SEED_META_DATA = safe_meta_search(SEED_URL)
headline = SEED_META_DATA['headline']
search_queries = list(SEED_META_DATA['top_phrases'].keys())

for query in search_queries:
    print(f"CHILD: {query}")
    results = google_search(query, my_api_key, my_cse_id, num=SEARCH_FORWARD)
    if (results == {}):
        continue
    for res in results:
        print(f"> Result Scan: {res}")
        child_url = res['link']
        child_meta_data = safe_meta_search(child_url)

# EOF
