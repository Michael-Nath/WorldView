# @Author: shounak
# @Date:   2022-02-19T04:05:55-08:00
# @Email:  shounak@stanford.edu
# @Filename: the_glue.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T23:20:46-08:00

def _set_cwd():
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
# _set_cwd()

<<<<<<< HEAD
# import scraping, nlp
from extraction import scraping, nlp
=======
# from backend import scraping, nlp
import scraping, nlp
from util import _print
>>>>>>> da4c6172c98e706ce3198ae23993d3cf2ae653d7

_print(f"{__file__}: DEPENDENCIES INSTALLED", 'LIGHTBLUE_EX')

def CORE_EXECUTION(NODE_URL: str) -> dict:
    # Get the meta data
    META_DATA: dict = scraping._GET_CONTENT(NODE_URL)
    _print(f"{__file__}: META DATA EXTRACTED", 'GREEN')
    assert META_DATA is not None

    # Analyze it
    ATTRIBUTES: dict = nlp._ANALYZE_META_DATA(META_DATA)
    _print(f"{__file__}: META DATA ANALYZED", 'GREEN')
    assert ATTRIBUTES is not None

    _print(f"{__file__}: SUCCESFULLY EXECUTED", 'LIGHTGREEN_EX')
    return ATTRIBUTES

def SIMILARITY_HELPER(NODE_URL: str):
    META_DATA = scraping._GET_CONTENT(NODE_URL)
    return nlp.GET_CONTENT(META_DATA)

"""TEST"""
# URL = "https://www.reuters.com/world/europe/shelling-breaks-out-east-ukraine-west-moscow-dispute-troop-moves-2022-02-17/"
# _result = CORE_EXECUTION(URL)
# _bad = CORE_EXECUTION("sdfsjdfknns.cas")

# REQUIREMENTS.TXT

# EOF
