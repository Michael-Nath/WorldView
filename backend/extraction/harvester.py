# @Author: shounak
# @Date:   2022-02-19T15:52:24-08:00
# @Email:  shounak@stanford.edu
# @Filename: harvester.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T16:55:26-08:00

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
import search_engines
from search_engines import google_search
import requests

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""
STD_THRESH = 0.3
SEED_URL = "https://www.cnn.com/travel/article/pandemic-travel-news-norway-lithuania-lift-restrictions/index.html"

_ = """
####################################################################################################
############################################ DEFINITIONS ###########################################
#################################################################################################"""

SEED_META_DATA = GET_META_DATA(SEED_URL)

url = google_search.get_search_url(SEED_META_DATA['headline'])
response = valid_getreq(url)
html = response.text
results, next_page_url = bing_search.extract_search_results(html, url)

# EOF
