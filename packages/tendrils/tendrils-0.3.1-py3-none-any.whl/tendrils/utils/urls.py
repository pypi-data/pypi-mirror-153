"""
For setting up and accessing remote urls. Defaults to FLOWS project ones but you can set up your own.
"""
from dataclasses import dataclass, asdict
import configparser
from tendrils.utils.config import load_config
from typing import Optional
from warnings import warn
import requests


@dataclass
class RemoteUrls:
    base_url: str = 'https://flows.phys.au.dk/api/'
    datafiles_url: str = 'datafiles.php'
    targets_url: str = 'targets.php'
    sites_url: str = 'sites.php'
    set_photometry_status_url: str = 'set_photometry_status.php'
    photometry_url: str = 'download_photometry.php'
    photometry_upload_url: str = 'upload_photometry.php'
    cleanup_photometry_status_url: str = 'cleanup_photometry_status.php'
    catalogs_url: str = 'reference_stars.php'
    catalogs_missing_url: str = 'catalog_missing.php'
    filters_url: str = 'filters.php'
    lightcurves_url: str = 'lightcurve.php'
    targets_post_url: str = 'targets_add.php'

    # def __post_init__(self):
    #    self.urls = [field.name for field in ]
    @staticmethod
    def urls_from_config(config: Optional[configparser.ConfigParser] = None) -> dict:
        """
        Update default remote urls with values found from config. Will warn if ALL values are not found.
        Returns: dict[str:str] representing urls
        These should be under a [URLS] section in config.ini or in another config.
        """
        if config is None:
            config = load_config()

        return dict(config['URL'])

    def update(self, new: Optional[dict] = None) -> None:
        for key, value in new.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                warn(f'{key} was given with value: {value} but is not one of {asdict(self).keys()}')

    def make_convenient(self) -> None:
        for key, value in asdict(self).items():
            if 'base_url' not in key:
                setattr(self, key, self.base_url + value)


def urls(urls_instance: Optional[RemoteUrls] = None) -> RemoteUrls:
    """
        Convenience function for getting an RemoteUrls instance.
        Warning! Destructively overrides all urls that are not "base_url"
        Returns: RemoteUrls , but with base_url prepended.
        """
    if urls_instance is None:
        urls_instance = RemoteUrls()  # Create default if not given
    urls_instance.make_convenient()
    return urls_instance


def urls_from_config(config: Optional[configparser.ConfigParser] = None) -> RemoteUrls:
    """
    Use config to return RemoteUrls instance with values read from default config or given ConfigParser instance.
    returned RemoteUrls have base_url prepended, similar to urls().
    Args:
        config: Optional[ConfigParser] instance which defaults to None. Uses default config if None.

    Returns: RemoteUrls instance with the urls populated from the given config
    """
    _urls = RemoteUrls()
    new_urls_dict = RemoteUrls.urls_from_config(config)
    _urls.update(new_urls_dict)
    return urls(_urls)


def get_request(url: str, token: str = None, params: Optional[dict] = None,
                headers: Optional[dict] = None) -> requests.Response:
    """
    Make a get request using request with given url, params, and header. Token can be given inplace of header
    to create a default header that uses the token.
    Args:
        url: str = url for get request
        token: Optional[str] = api token. Can also be provided as part of headers dict.
        params: Optional[dict] = dict of params
        headers: Optional[dict] = headers dict. Can also be created from just the token.

    Returns: requests.Response

    """
    params = {} if params is None else params
    headers = {} if headers is None else headers
    if not headers and token is None:
        warn('headers and token was None but one should probably give the authorization token')
    elif token is not None:
        headers['Authorization'] = 'Bearer ' + token

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response


def post_request(url: str, token: str = None, params: Optional[dict] = None, data: Optional[dict] = None,
                 headers: Optional[dict] = None, files: Optional[dict] = None) -> requests.Response:
    """
    Make a post request using request with given url, params, and header. Token can be given inplace of header
    to create a default header that uses the token.
    Args:
        url: str = url for get request
        token: str, optional = api token. Can also be provided as part of headers dict.
        params: dict, optional = dict of params
        data: dict, optional = dict of data
        headers: dict, optional = headers dict. Can also be created from just the token.
        files: dict, optional = files dict.

    Returns: requests.Response
    """
    data = {} if data is None else data
    params = {} if params is None else params
    files = {} if files is None else files
    headers = {} if headers is None else headers
    if not headers and token is None:
        warn('headers and token was None but one should probably give the authorization token')
    elif token is not None:
        headers['Authorization'] = 'Bearer ' + token

    response = requests.post(url, data=data, params=params, files=files, headers=headers)
    response.raise_for_status()
    return response
