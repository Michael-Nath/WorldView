# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T00:50:07-08:00
# @Description: Scrapes the headers and text body from all the files.
#               Most basic, source information needed. No abstraction.

import os
from typing import Final
# For visualizations
import trafilatura
import nltk
from nltk.corpus import stopwords
status = nltk.download('stopwords')
if not status:
    raise FileExistsError("FATAL: Can't install stopwords from NLTK. Uknown why.")
from nltk.tokenize import word_tokenize

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

# Data Processing Hyperparameters
TEST_URL = "https://www.reuters.com/world/europe/shelling-breaks-out-east-ukraine-west-moscow-dispute-troop-moves-2022-02-17/"

_ = """
####################################################################################################
############################################ DEFINTIONS ############################################
#################################################################################################"""

def word_list(URL):
    downloaded = trafilatura.fetch_url(URL)
    content = trafilatura.extract(downloaded)
    words = set([s.strip() for s in content.split()])

    return words

# EOF
