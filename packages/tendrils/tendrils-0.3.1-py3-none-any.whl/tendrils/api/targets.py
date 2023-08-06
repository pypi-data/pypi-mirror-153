"""
Get information about targets in Flows.
Add target to Flows.
"""

import re
from datetime import datetime
from functools import lru_cache
from typing import Union, Optional
from astropy.time import Time
from astropy.coordinates import SkyCoord
from tendrils.utils import get_api_token, get_request, URLS, resolve_date_iso, post_request

@lru_cache(maxsize=10)
def get_target(target: Union[int, str]) -> dict:
    """
    Get target as json
    Args:
        target: Optional[int, str] targetid

    Returns: json of target info

    """
    token = get_api_token()
    r = get_request(URLS.targets_url, token=token, params={'target': target})
    jsn = r.json()

    # Parse some of the fields to Python objects:
    jsn['inserted'] = datetime.strptime(jsn['inserted'], '%Y-%m-%d %H:%M:%S.%f')
    if jsn['discovery_date']:
        jsn['discovery_date'] = Time(jsn['discovery_date'], format='iso', scale='utc')

    return jsn


@lru_cache(maxsize=1)
def get_targets() -> dict:
    """
    Get json list of all targets and some basic info about them
    Returns: json list of all targets

    """
    token = get_api_token()
    r = get_request(URLS.targets_url, token=token)
    jsn = r.json()

    # Parse some of the fields to Python objects:
    for tgt in jsn:
        tgt['inserted'] = datetime.strptime(tgt['inserted'], '%Y-%m-%d %H:%M:%S.%f')
        if tgt['discovery_date']:
            tgt['discovery_date'] = Time(tgt['discovery_date'], format='iso', scale='utc')

    return jsn


def add_target(name: str,
               coord: SkyCoord,
               redshift: Optional[float] = None,
               redshift_error: Optional[float] = None,
               discovery_date: Union[Optional[Time], Optional[datetime], Optional[str]] = None,
               discovery_mag: Union[Optional[float], Optional[int]] = None,
               host_galaxy: Optional[str] = None,
               ztf: Optional[str] = None,
               sntype: Optional[str] = None,
               status: str = 'candidate',
               project: str = 'flows') -> int:
    """
    Add new candidate or target.

    Coordinates are specified using an Astropy SkyCoord object, which can be
    created in the following way:

    coord = SkyCoord(ra=19.1, dec=89.00001, unit='deg', frame='icrs')

    The easiest way is to specify ``discovery_date`` as an Astropy Time object:

    discovery_date = Time('2020-01-02 00:00:00', format='iso', scale='utc')

    Alternatively, you can also specify it as a :class:`datetime.datetime` object,
    but some care has to be taken with specifying the correct timezone:

    discovery_date = datetime.strptime('2020-01-02 00:00:00', '%Y-%m-%d %H:%M:%S%f')
    discovery_date = pytz.timezone('America/New_York').localize(discovery_date)

    Lastly, it can be given as a simple date-string of the following form,
    but here the data has to be given in UTC:

    discovery_date = '2020-01-02 23:56:02.123'

    Parameters:
        name (str): Name of target. Must be of the form "YYYYxyz", where YYYY is the year,
            and xyz are letters.
        coord (:class:ʼastropy.coordinates.SkyCoordʼ): Sky coordinates of target.
        redshift (float, optional): Redshift.
        redshift_error (float, optional): Uncertainty on redshift.
        discovery_date (:class:`astropy.time.Time`, :class:`datetime.datetime` or str, optional):
        discovery_mag (float, int, optional): Magnitude at time of discovery.
        host_galaxy (str, optional): Host galaxy name.
        sntype (str, optional): Supernovae type (e.g. Ia, Ib, II).
        ztf (str, optional): ZTF identifier.
        status (str, optional):
        project (str, optional):

    Returns:
        int: New target identifier in Flows system.
    """
    # Check and convert input:
    if not re.match(r'^[12]\d{3}([A-Z]|[a-z]{2,4})$', name.strip()):
        raise ValueError("Invalid target name.")

    if redshift is None and redshift_error is not None:
        raise ValueError("Redshift error specified without redshift value")

    discovery_date = resolve_date_iso(discovery_date)  # Get as UTC iso string, raises if invalid
    discovery_mag = float(discovery_mag) if discovery_mag is not None else discovery_mag

    if status not in ('candidate', 'target'):
        raise ValueError("Invalid target status.")

    token = get_api_token()

    # Gather parameters to be sent to API:
    params = {'targetid': 0, 'target_name': name.strip(), 'ra': coord.icrs.ra.deg, 'decl': coord.icrs.dec.deg,
              'redshift': redshift, 'redshift_error': redshift_error, 'discovery_date': discovery_date,
              'discovery_mag': discovery_mag, 'host_galaxy': host_galaxy, 'project': project, 'ztf_id': ztf,
              'target_status': status, 'sntype': sntype}

    # Post the request to the API:
    r = post_request(URLS.targets_post_url, token=token, data=params)
    jsn = r.json()

    # Check for errors:
    if jsn['errors'] is not None:
        raise RuntimeError(f"Adding target '{name}' resulted in an error: {jsn['errors']}")

    return int(jsn['targetid'])
