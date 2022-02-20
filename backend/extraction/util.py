# @Author: shounak
# @Date:   2022-02-19T00:57:01-08:00
# @Email:  shounak@stanford.edu
# @Filename: util.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T16:54:32-08:00

# Purpose: utility functions

import nltk
import requests

def download_nltk_dependecy(dep):
    status = nltk.download(dep)
    if not status:
        raise FileExistsError("FATAL: Can't install stopwords from NLTK. Unknown why.")

def valid_getreq(URL: str):
    can_get = None
    try:
        can_get = requests.get(URL)
    except:
        raise KeyError(f"Invalid URL: {URL}")

    if can_get.status_code != 200 or can_get is None:
        raise KeyError("FATAL: Unable to open URL.")

    return can_get

def safe_request(URL: str, API_TOKEN = None) -> [None, dict]:
    _response = valid_getreq(URL)
    API_CALL: str = f"https://api.diffbot.com/v3/article?token={API_TOKEN}&url={URL}&maxTags=0"
    print(f"{__file__}: URL VALIDATED")
    return requests.get(API_CALL)
