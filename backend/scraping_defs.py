# @Author: shounak
# @Date:   2022-02-18T23:25:20-08:00
# @Email:  shounak@stanford.edu
# @Filename: scraping_defs.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T00:10:29-08:00
# @Description: Scrapes the headers and text body from all the files.
#               Most basic, source information needed. No abstraction.

import ast
import collections
import math
import os
# For Graph Traversal
import random
# Regex Library
import re
import time
import webbrowser
from collections import Counter
from typing import Final
# For visualizations
from itertools import chain
from math import cos, radians, sin
from pathlib import Path
import matplotlib
# import tkinter
# tkinter._test()
# import nest_asyncio
# nest_asyncio.apply()
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
# For colormind integration
from webdriver_manager.chrome import ChromeDriverManager

_ = """
####################################################################################################
########################################## HYPERPARAMETERS #########################################
#################################################################################################"""

# Data Processing Hyperparameters
FULL_SCROLL_NUMBER = 10
TEST_URL = "https://www.nytimes.com/2022/02/12/us/politics/donald-trump-business-interests.html"
SCROLL_MAX = 4
TIMEOUT_THRESH = 10

_ = """
####################################################################################################
############################################ DEFINTIONS ############################################
#################################################################################################"""

def check_exists_by_xpath(xpath, driver):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def open_tab(driver):
    driver.execute_script("window.open('');")
    driver.switch_to_window(driver.window_handles[-1])


def close_tab(driver):
    driver.execute_script("window.close('');")
    driver.switch_to_window(driver.window_handles[-1])



_ = """
####################################################################################################
############################################# SCRAPING #############################################
#################################################################################################"""

# Initiate scraping session
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(TEST_URL)
time.sleep(5.0)

_ = """
####################################################################################################
######################################### DATA PROCESSING ##########################################
#################################################################################################"""


# EOF
