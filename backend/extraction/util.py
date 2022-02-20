# @Author: shounak
# @Date:   2022-02-19T00:57:01-08:00
# @Email:  shounak@stanford.edu
# @Filename: util.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T16:42:28-08:00

# Purpose: utility functions

import nltk
import requests

def download_nltk_dependecy(dep):
    status = nltk.download(dep)
    if not status:
        raise FileExistsError("FATAL: Can't install stopwords from NLTK. Unknown why.")

def safe_request(URL: str, API_TOKEN: str) -> [None, dict]:
    API_CALL: str = f"https://api.diffbot.com/v3/article?token={API_TOKEN}&url={URL}&maxTags=0"
    try:
        print(URL)
        can_get = requests.get(URL)
    except:
        raise KeyError(f"Invalid URL: {URL}")

    if can_get.status_code != 200:
        raise KeyError("FATAL: Unable to open URL.")
    print(f"{__file__}: URL VALIDATED")
    return requests.get(API_CALL)
