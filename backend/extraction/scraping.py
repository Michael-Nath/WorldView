# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-20T00:51:30-08:00
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
<<<<<<< HEAD
from extraction.util import safe_request
# from util import safe_request
=======
from util import safe_request, _print
import urllib.parse
>>>>>>> da4c6172c98e706ce3198ae23993d3cf2ae653d7

_print(f"{__file__}: DEPENDENCIES INSTALLED", 'LIGHTBLUE_EX')

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

# URL = "https://www.latimes.com/projects/california-coronavirus-cases-tracking-outbreak/covid-19-vaccines-distribution/"
# requests.get(URL)

def _GET_CONTENT(URL: str) -> dict:
    response = safe_request(URL, API_TOKEN=API_TOKEN)
    information: str = response.json()
    if "objects" not in information.keys():
        return {}
    information = information['objects'][0]
    _print(information, 'CYAN')
    _content = information['text']
    _content = '\n'.join(list(chain.from_iterable([l.split(". ") for l in _content.split('\n')])))

    return {'url': URL,
            'headline': information['title'],
            'author': information.get('author'),
            'date': information.get('date'),
            'content': _content}

# response = safe_request(URL, API_TOKEN=API_TOKEN)
# response.json()
# EOF
