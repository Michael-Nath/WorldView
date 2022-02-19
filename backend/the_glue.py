# @Author: shounak
# @Date:   2022-02-19T04:05:55-08:00
# @Email:  shounak@stanford.edu
# @Filename: the_glue.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-19T04:33:31-08:00

from typing import Final, Union
from backend import scraping, nlp

def CORE_EXECUTION(NODE_URL: str) -> dict:
    # Get the meta data
    META_DATA: Union[Final, dict] = scraping._GET_CONTENT(NODE_URL)
    assert META_DATA is not None

    # Analyze it
    ATTRIBUTES: Union[Final, dict] = nlp._ANALYZE_META_DATA(META_DATA)
    assert ATTRIBUTES is not None

    return ATTRIBUTES

"""TEST"""
# URL = "https://www.reuters.com/world/europe/shelling-breaks-out-east-ukraine-west-moscow-dispute-troop-moves-2022-02-17/"
# _result = CORE_EXECUTION(URL)
# print(list(_result.keys()))

# EOF
