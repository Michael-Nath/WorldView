# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T01:18:52-08:00
# @Description: Scrapes the headers and text body from all the files.
#               Most basic, source information needed. No abstraction.

import os
from typing import Final
# For visualizations
from trafilatura import fetch_url, extract

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

def get_content(URL):
    return extract(fetch_url(URL))

# EOF
