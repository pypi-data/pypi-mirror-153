"""
For querying photometric filters.
"""

from functools import lru_cache
import astropy.units as u
from tendrils.utils import get_api_token, get_request, URLS


@lru_cache(maxsize=10)
def get_filters() -> dict:
    """
    Get all filters
    Returns: json of filters as python dict

    """
    token = get_api_token()
    r = get_request(URLS.filters_url, token=token)
    jsn = r.json()

    # Add units:
    for f, val in jsn.items():
        if val.get('wavelength_center'):
            val['wavelength_center'] *= u.nm
        if val.get('wavelength_width'):
            val['wavelength_width'] *= u.nm

    return jsn
