# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T04:03:46-08:00
# @Description: Scrapes the headers and text body from all the files.
#               Most basic, source information needed. No abstraction.

import os
from typing import Final
# For visualizations
from trafilatura import fetch_url, extract
import requests

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

# Data Processing Hyperparameters
TEST_URL: Final = "https://www.reuters.com/world/europe/shelling-breaks-out-east-ukraine-west-moscow-dispute-troop-moves-2022-02-17/"
API_TOKEN: Final = "98cae39602266658db397fa5fc7cc550"

_ = """
####################################################################################################
############################################ DEFINTIONS ############################################
#################################################################################################"""

def get_content(URL):
    return extract(fetch_url(URL))

def get_content(URL):
    API_CALL = f"https://api.diffbot.com/v3/article?token={API_TOKEN}&url={URL}&maxTags=0"
    if (response := requests.get(API_CALL)).status_code != 200:
        raise KeyError("FATAL: Unable to open URL.")
    information = response.json()['objects'][0]
    return {'headline': information['title'],
            'author': information['author'],
            'date': information['date'],
            # 'sentiment': information['sentiment'],
            'content': information['text']}

get_content(TEST_URL)

# EOF
