# @Author: shounak
# @Date:   2022-02-19T00:38:39-08:00
# @Email:  shounak@stanford.edu
# @Filename: extracontent.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T18:53:55-08:00

# NOTE: Do not run this file. It's purpose is to track helpful snippets.


"""TRADITIONAL SCRAPING MECHANISM"""
{
# import tkinter
# tkinter._test()
# import nest_asyncio
# nest_asyncio.apply()
# import requests
# import bs4
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from webdriver_manager.chrome import ChromeDriverManager

# Initiate scraping session
# SCROLL_MAX = 4
# TIMEOUT_THRESH = 10
# GRACE = 5;
# FULL_SCROLL_NUMBER = 10

# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--kiosk")
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# load(driver, TEST_URL)

# def load(driver, url, val_xpath=None, validate=False, TIMEOUT_THRESH=TIMEOUT_THRESH, GRACE=GRACE):
#     if(val_xpath is not None):
#         validate = True
#     driver.get(url)
#     if(validate):
#         util_validate(driver, val_xpath)
#     time.sleep(GRACE)
#
# def check_exists_by_xpath(xpath, driver):
#     try:
#         driver.find_element_by_xpath(xpath)
#     except NoSuchElementException:
#         return False
#     return True
#
# def open_tab(driver):
#     driver.execute_script("window.open('');")
#     driver.switch_to_window(driver.window_handles[-1])
#
# def close_tab(driver):
#     driver.execute_script("window.close('');")
#     driver.switch_to_window(driver.window_handles[-1])
#
# def util_validate(driver, xpath, TIMEOUT_THRESH=TIMEOUT_THRESH):
#     try:
#         WebDriverWait(driver, TIMEOUT_THRESH).until(EC.presence_of_element_located((By.XPATH, xpath)))
#     except TimeoutException:
#         print('Page timed out after ' + str(TIMEOUT_THRESH) + ' seconds during validation.')
}

"""GRAPHING"""
{
# def series_to_graph(series, level_name='ID', graph_type='Graph'):
#     G = getattr(nx, graph_type)()
#     for id in series.index.get_level_values(level_name).unique():
#         group_dst = series.loc[id]
#         new_group_dst = []
#         for group, freq in group_dst.items():
#             new_group_dst.extend([group] * freq)
#         G.add_edges_from(combinations(new_group_dst, 2))
#     return G
}

"""NLP"""
{
# with open('backend/ref/pos_fullform.txt') as f:
#     POS_MAP = dict([l.replace('\n', '').split(' ', 1) for l in f.readlines()])
# content_obj = nltk.Text(all_clean_words)
# concordances = [e.line for e in content_obj.concordance_list("putin", lines=5)]
# list(nltk.corpus.state_union.words())
# type(concordances)

# from trafilatura import fetch_url, extract
# def get_content(URL):
#     return extract(fetch_url(URL))
}

"""HARVESTING"""
{
# from search_engine_parser import GoogleSearch
# import nest_asyncio
# nest_asyncio.apply()
# import pprint
# from search_engines import google_search
}

"""EOF"""
