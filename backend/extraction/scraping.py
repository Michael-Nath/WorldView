# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T19:45:41-08:00
# @Description: Scrapes the headers and text body from all the files.
#               Most basic, source information needed. No abstraction.

# def _set_cwd():
#     import os
#     abspath = os.path.abspath(__file__)
#     dname = os.path.dirname(abspath)
#     os.chdir(dname)
# _set_cwd()

import requests
from itertools import chain
from util import safe_request
import urllib.parse

print(f"{__file__}: DEPENDENCIES INSTALLED")

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

# Data Processing Hyperparameters
API_TOKEN: str = """98cae39602266658db397fa5fc7cc550"""

_ = """
####################################################################################################
############################################ DEFINTIONS ############################################
#################################################################################################"""

URL = "https://news.yahoo.com/putin-may-launch-invasion-of-ukraine-in-donbas-region-analysts-say-230334521.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAJWUdlVJYte_fqKUCN8sXeSawpxNrgwa7k43-xTUHphQ-H6rpph6kJB_Ayww4JIW06pwZuQniqbz65rivtY0u4221xC2_GQLPMjRG6Ku2m78rzM3ol-qQ1LMjdB0Zjs23AjO_wDIQ5Si7Gq-s8-rcYMo6RqEcEuUElItj9KfGgyD"

def _GET_CONTENT(URL: str) -> dict:
    response = safe_request(URL, API_TOKEN=API_TOKEN)
    information: str = response.json()
    if "objects" not in information.keys():
        return {}
    information = information['objects'][0]
    _content = information['text']
    _content = '\n'.join(list(chain.from_iterable([l.split(". ") for l in _content.split('\n')])))

    return {'url': URL,
            'headline': information['title'],
            'author': information['author'],
            'date': information['date'],
            'content': _content}

response = safe_request(URL, API_TOKEN=API_TOKEN)
response.json()
# EOF
