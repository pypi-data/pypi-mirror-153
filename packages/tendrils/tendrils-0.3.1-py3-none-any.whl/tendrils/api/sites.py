"""
For querying site information
"""

from functools import lru_cache
import astropy.units as u
from astropy.coordinates import EarthLocation
from tendrils.utils import get_api_token, get_request, URLS
from typing import Union


@lru_cache(maxsize=10)
def get_site(siteid: Union[int, str]) -> dict:
    """
    Get site information (defined per each instrument).
    Args:
        siteid: Optional[int, str] site id number.

    Returns: json of site (instrument) parameters.

    """
    token = get_api_token()
    r = get_request(URLS.sites_url, token=token, params={'siteid': siteid})
    jsn = r.json()

    # Special derived objects:
    jsn['EarthLocation'] = EarthLocation(lat=jsn['latitude'] * u.deg, lon=jsn['longitude'] * u.deg,
                                         height=jsn['elevation'] * u.m)
    return jsn


@lru_cache(maxsize=1)
def get_all_sites() -> dict:
    """
    Get info for all sites registered in FLOWS
    Returns: json of site (instrument) parameters.

    """
    token = get_api_token()
    r = get_request(URLS.sites_url, token=token)
    jsn = r.json()

    # Special derived objects:
    for site in jsn:
        site['EarthLocation'] = EarthLocation(lat=site['latitude'] * u.deg, lon=site['longitude'] * u.deg,
                                              height=site['elevation'] * u.m)
    return jsn
