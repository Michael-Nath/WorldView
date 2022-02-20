# @Author: shounak
# @Date:   2022-02-19T15:52:24-08:00
# @Email:  shounak@stanford.edu
# @Filename: harvester.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T17:27:26-08:00

# def _set_cwd():
#     import os
#     abspath = os.path.abspath(__file__)
#     dname = os.path.dirname(abspath)
#     os.chdir(dname)
# _set_cwd()

from backend.extraction.core_extraction import CORE_EXECUTION as GET_META_DATA
from backend.extraction.util import safe_request, valid_getreq
# import extraction.core_extraction as SINGLE_EXTRACTION
# from extraction.util import safe_request, check_validity
import numpy as np
# import search_engines
# from search_engines import google_search
import requests
# from googleapiclient.discovery import build
from search_engine_parser import GoogleSearch
import nest_asyncio
nest_asyncio.apply()
# import pprint

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""
STD_THRESH = 0.3
SEED_URL = "https://www.foxnews.com/sports/penn-lia-thomas-yale-iszac-henig-ivy-championships-100-free"

_ = """
####################################################################################################
############################################ DEFINITIONS ###########################################
#################################################################################################"""

def google(query):
    search_args = (query, 1)
    gsearch = GoogleSearch()
    gresults = gsearch.search(*search_args)
    return gresults['links']

SEED_META_DATA = GET_META_DATA(SEED_URL)

SEED_META_DATA['top_phrases']

query = SEED_META_DATA['headline']
search_args = (query, 1)
gsearch = GoogleSearch()
gresults = gsearch.search(*search_args)
gresults.results

google(SEED_META_DATA['headline'])

# url = google_search.get_search_url(SEED_META_DATA['headline'])



# EOF
