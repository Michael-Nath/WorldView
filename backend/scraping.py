# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T04:30:39-08:00
# @Description: Scrapes the headers and text body from all the files.
#               Most basic, source information needed. No abstraction.

import requests
from typing import Final

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

# Data Processing Hyperparameters
API_TOKEN: Final = """98cae39602266658db397fa5fc7cc550"""

_ = """
####################################################################################################
############################################ DEFINTIONS ############################################
#################################################################################################"""

def safe_request(URL: str) -> [None, dict]:
    API_CALL: Final = f"https://api.diffbot.com/v3/article?token={API_TOKEN}&url={URL}&maxTags=0"
    if (response := requests.get(API_CALL)).status_code != 200:
        raise KeyError("FATAL: Unable to open URL.")
    return response

def _GET_CONTENT(URL: str) -> dict:
    response = safe_request(URL)
    information: Final = response.json()['objects'][0]

    return {'url': URL,
            'headline': information['title'],
            'author': information['author'],
            'date': information['date'],
            'content': information['text']}

# EOF
