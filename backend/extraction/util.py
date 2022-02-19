# @Author: shounak
# @Date:   2022-02-19T00:57:01-08:00
# @Email:  shounak@stanford.edu
# @Filename: util.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T01:03:59-08:00

# Purpose: utility functions

import nltk

def download_nltk_dependecy(dep):
    status = nltk.download(dep)
    if not status:
        raise FileExistsError("FATAL: Can't install stopwords from NLTK. Unknown why.")
