# @Author: shounak
# @Date:   2022-02-19T04:05:55-08:00
# @Email:  shounak@stanford.edu
# @Filename: the_glue.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T15:49:03-08:00

def _set_cwd():
    import os
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
_set_cwd()

# from backend import scraping, nlp
import scraping, nlp

print(f"{__file__}: DEPENDENCIES INSTALLED")

def CORE_EXECUTION(NODE_URL: str) -> dict:
    # Get the meta data
    META_DATA: dict = scraping._GET_CONTENT(NODE_URL)
    print(f"{__file__}: META DATA EXTRACTED")
    assert META_DATA is not None

    # Analyze it
    ATTRIBUTES: dict = nlp._ANALYZE_META_DATA(META_DATA)
    print(f"{__file__}: META DATA ANALYZED")
    assert ATTRIBUTES is not None

    print(f"{__file__}: SUCCESFULLY EXECUTED")
    return ATTRIBUTES

"""TEST"""
# URL = "https://www.reuters.com/world/europe/shelling-breaks-out-east-ukraine-west-moscow-dispute-troop-moves-2022-02-17/"
# _result = CORE_EXECUTION(URL)
# _bad = CORE_EXECUTION("sdfsjdfknns.cas")

# REQUIREMENTS.TXT

# EOF
