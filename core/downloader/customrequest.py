"""
    special_get fetch with special strategy
    to handle http responses & possible errors
"""
from time import sleep
import requests


def special_get(url, payload, tries=3):
    """
    url : url to request
    payload : json params
    tries : nb to try
    """
    do_retry = False
    response = None

    if tries > 0:
        try:
            response = requests.get(url, params=payload)
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            do_retry = True
        except:
            raise

        if do_retry or response.status_code >= 500:
            sleep(300)
            return special_get(url, payload, tries - 1)

    return response
