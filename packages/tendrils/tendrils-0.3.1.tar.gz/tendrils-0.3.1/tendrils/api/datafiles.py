"""
Functions for accessing flows datafiles from a remote server
"""

from datetime import datetime
from functools import lru_cache
from typing import Union, Optional
from tendrils.utils import get_api_token, get_request, URLS

@lru_cache(maxsize=10)
def get_datafile(fileid: Union[int, str]):
    """
    Get single datafile
    Args:
        fileid: fileid to query

    Returns: json of datafile
    """
    token = get_api_token()
    r = get_request(URLS.datafiles_url, token=token, params={'fileid': fileid})
    jsn = r.json()

    # Parse some of the fields to Python objects:
    jsn['inserted'] = datetime.strptime(jsn['inserted'], '%Y-%m-%d %H:%M:%S.%f')
    jsn['lastmodified'] = datetime.strptime(jsn['lastmodified'], '%Y-%m-%d %H:%M:%S.%f')

    return jsn


def get_datafiles(targetid: Optional[int] = None,
                  filt: str = 'missing',
                  minversion: Optional[str] = None) -> list[int]:
    """
    Get list of data file IDs to be processed.

    Parameters:
        targetid (int, optional): Target ID to process.
        filt (str, optional): Filter the returned list:
            - ``missing``: Return only data files that have not yet been processed.
            - ``'all'``: Return all data files.
        minversion (str, optional): Special filter matching files not processed at least with
            the specified version (defined internally in API for now).

    Returns:
        list: List of data files the can be processed.
    """

    # Validate input:
    if filt not in ('missing', 'all', 'error'):
        raise ValueError("Invalid filter specified: '%s'" % filt)

    token = get_api_token()

    params = {}
    if targetid is not None:
        params['targetid'] = targetid
    if minversion is not None:
        params['minversion'] = minversion
    params['filter'] = filt

    r = get_request(URLS.datafiles_url, token=token, params=params)
    return r.json()
