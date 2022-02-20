# @Author: shounak
# @Date:   2022-02-19T00:57:01-08:00
# @Email:  shounak@stanford.edu
# @Filename: util.py
# @Last modified by:   shounak
# @Last modified time: 2022-02-20T05:06:10-08:00

# Purpose: utility functions

import nltk
import requests
import signal
from contextlib import contextmanager
from colorama import Fore, Style

class TimeoutException(Exception): pass

def _print(txt: str, color: str = 'LIGHTGREEN_EX') -> None:
    """Custom print function with optional colored text.
    Parameters
    ----------
    txt : str
        The content of the print statement (must be a text, not any other data structure).
    color : str
        The desired color of the message. This must be compatible with the colorama.Fore package.
        SEE: https://pypi.org/project/colorama/
    Returns
    -------
    None
        While nothing is returned, this function prints to the console.
    """
    fcolor = color.upper()
    if(type(txt) == str):
        # Format the provided string
        txt = txt.replace("'", "\\'").replace('"', '\\"')
        output = f'print(Fore.{fcolor} + """{txt}""" + Style.RESET_ALL)'
        # Print the specified string to the console
    else:
        output = f'print(Fore.{fcolor}, {txt}, Style.RESET_ALL)'
    exec(output)

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def download_nltk_dependecy(dep):
    status = nltk.download(dep)
    if not status:
        raise FileExistsError("FATAL: Can't install stopwords from NLTK. Unknown why.")

def valid_getreq(URL: str):
    can_get = None
    try:
        can_get = requests.get(URL)
        _print(f"REQUEST STATUS: {can_get}", 'LIGHTMAGENTA_EX')
    except Exception as e:
        _print(f"Exception: {e}", 'RED')
        raise KeyError(f"Invalid URL: {URL}")

    if can_get.status_code != 200 or can_get is None:
        raise KeyError("FATAL: Unable to open URL.")

    return can_get

def safe_request(URL: str, API_TOKEN = None) -> [None, dict]:
    _response = valid_getreq(URL)
    API_CALL: str = f"https://api.diffbot.com/v3/article?token={API_TOKEN}&url={URL}&maxTags=0"
    _print(f"{__file__}: URL VALIDATED", 'GREEN')
    return requests.get(API_CALL)
