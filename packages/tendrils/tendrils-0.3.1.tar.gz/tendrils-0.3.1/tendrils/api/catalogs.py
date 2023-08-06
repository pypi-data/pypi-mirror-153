"""
Get FLOWS specific catalogs.
"""

from functools import lru_cache
import astropy.units as u
from astropy.table import Table
from astropy.time import Time
from typing import Union, Optional
from tendrils.utils import get_api_token, get_request, URLS
from enum import Enum


class OutputFormat(Enum):
    table = 'table'
    dictionary = 'dict'
    json = 'json'


def create_catalog_table(jsn: dict) -> dict:
    dict_tables: dict[str, Table] = {}

    tab = Table(names=(
        'targetid', 'target_name', 'target_status', 'ra', 'decl', 'redshift', 'redshift_error', 'discovery_mag',
        'catalog_downloaded', 'pointing_model_created', 'inserted', 'discovery_date', 'project', 'host_galaxy',
        'ztf_id', 'sntype'), dtype=(
        'int32', 'str', 'str', 'float64', 'float64', 'float32', 'float32', 'float32', 'bool', 'bool', 'object',
        'object', 'str', 'str', 'str', 'str'), rows=[jsn['target']])

    tab['ra'].description = 'Right ascension'
    tab['ra'].unit = u.deg
    tab['decl'].description = 'Declination'
    tab['decl'].unit = u.deg
    dict_tables['target'] = tab

    for table_name in ('references', 'avoid'):
        tab = Table(names=(
            'starid', 'ra', 'decl', 'pm_ra', 'pm_dec', 'gaia_mag', 'gaia_bp_mag', 'gaia_rp_mag', 'gaia_variability',
            'B_mag', 'V_mag', 'H_mag', 'J_mag', 'K_mag', 'u_mag', 'g_mag', 'r_mag', 'i_mag', 'z_mag', 'distance'),
            dtype=('int64', 'float64', 'float64', 'float32', 'float32', 'float32', 'float32', 'float32', 'int32',
                   'float32', 'float32', 'float32', 'float32', 'float32', 'float32', 'float32', 'float32', 'float32',
                   'float32', 'float64'), rows=jsn[table_name])

        tab['starid'].description = 'Unique identifier in REFCAT2 catalog'
        tab['ra'].description = 'Right ascension'
        tab['ra'].unit = u.deg
        tab['decl'].description = 'Declination'
        tab['decl'].unit = u.deg
        tab['pm_ra'].description = 'Proper motion in right ascension'
        tab['pm_ra'].unit = u.mas / u.yr
        tab['pm_dec'].description = 'Proper motion in declination'
        tab['pm_dec'].unit = u.mas / u.yr
        tab['distance'].description = 'Distance from object to target'
        tab['distance'].unit = u.deg

        tab['gaia_mag'].description = 'Gaia G magnitude'
        tab['gaia_bp_mag'].description = 'Gaia Bp magnitude'
        tab['gaia_rp_mag'].description = 'Gaia Rp magnitude'
        tab['gaia_variability'].description = 'Gaia variability classification'
        tab['B_mag'].description = 'Johnson B magnitude'
        tab['V_mag'].description = 'Johnson V magnitude'
        tab['H_mag'].description = '2MASS H magnitude'
        tab['J_mag'].description = '2MASS J magnitude'
        tab['K_mag'].description = '2MASS K magnitude'
        tab['u_mag'].description = 'u magnitude'
        tab['g_mag'].description = 'g magnitude'
        tab['r_mag'].description = 'r magnitude'
        tab['i_mag'].description = 'i magnitude'
        tab['z_mag'].description = 'z magnitude'

        # Add some meta-data to the table as well:
        tab.meta['targetid'] = int(dict_tables['target']['targetid'])

        dict_tables[table_name] = tab
        return dict_tables


@lru_cache(maxsize=10)
def get_catalog(target: Union[int, str], radius: Optional[float] = None, output: str = 'table') -> dict:
    """

    Parameters:
        target (int or str):
        radius (float, optional): Radius around target in degrees to return targets for.
        output (str, optional): Desired output format. Choices are 'table', 'dict', 'json'.
            Default='table'.

    Returns:
        dict: Dictionary with three members:
            - 'target': Information about target.
            - 'references': Table with information about reference stars close to target.
            - 'avoid': Table with stars close to target which should be avoided in FOV selection.
    """
    output = OutputFormat(output)
    # make request
    token = get_api_token()
    r = get_request(URLS.catalogs_url, token=token, params={'target': target})
    jsn = r.json()

    # Convert timestamps to actual Time objects:
    jsn['target']['inserted'] = Time(jsn['target']['inserted'], scale='utc')
    if jsn['target']['discovery_date'] is not None:
        jsn['target']['discovery_date'] = Time(jsn['target']['discovery_date'], scale='utc')

    if radius is not None:
        pass  # Not implemented

    if output is not OutputFormat.table:
        return jsn
    return create_catalog_table(jsn)


def get_catalog_missing():
    """
    Get missing catalogs
    Returns: json of missing catalogs
    """
    token = get_api_token()
    r = get_request(URLS.catalogs_missing_url, token=token)
    return r.json()
