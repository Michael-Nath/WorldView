# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T15:35:36-08:00
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

def safe_request(URL: str) -> [None, dict]:
    API_CALL: str = f"https://api.diffbot.com/v3/article?token={API_TOKEN}&url={URL}&maxTags=0"
    try:
        can_get = requests.get(URL)
        if can_get.status_code != 200:
            raise KeyError("FATAL: Unable to open URL.")
    except:
        raise KeyError(f"Invalid URL: {URL}")
    print(f"{__file__}: URL VALIDATED")
    return requests.get(API_CALL)

def _GET_CONTENT(URL: str) -> dict:
    response = safe_request(URL)
    information: str = response.json()['objects'][0]
    _content = information['text']
    _content = '\n'.join(list(chain.from_iterable([l.split(". ") for l in _content.split('\n')])))

    return {'url': URL,
            'headline': information['title'],
            'author': information['author'],
            'date': information['date'],
            'content': _content}

# EOF
