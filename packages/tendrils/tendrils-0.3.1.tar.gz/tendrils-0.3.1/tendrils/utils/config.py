"""
Functions for dealing with configuration of Tendrils API using .ini files or secrets.
"""

import configparser
import os.path
from functools import lru_cache
from typing import Optional
from warnings import warn


@lru_cache(maxsize=1)
def load_config(filename: str = 'config.ini') -> configparser.ConfigParser:
    """
    Load configuration file. Defaults to searching for config.ini but a custom name can be given.

    Returns:
        ``configparser.ConfigParser``: Configuration file.

    .. codeauthor:: Rasmus Handberg <rasmush@phys.au.dk>
    .. codeauthor:: Emir Karamehmetoglu <emir.k@phys.au.dk>
    """

    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"{filename} file not found")

    config = configparser.ConfigParser()
    config.read(config_file)

    if config.get('api','token') == 'None':
        warn("Token could not be found! Try using 'set_api_token', 'create_config', or 'copy_from_other_config'")
    return config


def clear_config_cache():
    """
    Clear the config cache.
    """
    load_config.cache_clear()


def set_api_token(token: Optional[str] = None, filename: Optional[str] = 'config.ini', overwrite: bool = True) -> None:
    """
    For updating FLOWS API token.
    Args:
        token (str, optional): FLOWS api token
        filename (str): filename of config file, defaults to `config.ini`.
        overwrite (bool): Whether to overwrite the config if the field is not "None".
        True by default. Set to false if you don't want to overwrite if field is not "None".
    """
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    config = configparser.ConfigParser()
    config.read(config_file)

    if config.get('api', 'token') == "None" or overwrite:
        if token is None:
            token =  input('Enter API token to be saved into config:')
        config.set('api','token', token)

    with open(config_file, 'w') as cfgfile:
        config.write(cfgfile)

    clear_config_cache()


def update_api_token() -> str:
    """
    Update API token in config file via explicit query.
    """
    token = str(input('Tendrils needs your FLOWS API token. Please enter it:'))
    # We remove spaces from the token to avoid errors.
    token = token.strip().replace(' ', '')
    set_api_token(token, overwrite=True)
    print(f'Token with value {token} set and saved.\nIf there is a problem, please run Tendrils again.')
    return token


def get_api_token() -> str:
    """
    Get api token from config file or raise.
    Returns: str = token as a string

    """
    # Get API token from config file:
    config = load_config()
    token = config.get('api', 'token', fallback=None)

    if token is None:
        raise RuntimeError("No API token has been defined")

    if token.lower() in ['none', 'test', '', 'bad', 'bad_token', 'badtoken']:
        token = update_api_token()

    return token


def set_photometry_folders(output: Optional[str] = None, archive_local: Optional[str] = None,
                           filename: str = 'config.ini', overwrite:bool = True) -> None:
    """
    For updating FLOWS photometry output and local archive folders.
    Args:
        output (str, optional): path to desired photometry output directory.
        archive_local (str, optional): path to desired local archive directory.
        filename (str): default = 'config.ini'. Filename for config file
        overwrite (bool): Whether to overwrite existing field if field is not "None".
    """

    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    config = configparser.ConfigParser()
    config.read(config_file)

    if config.get('photometry', 'output') == "None" or overwrite:
        if output is None:
            config['photometry']['output'] = input('Enter photometry output directory absolute path:')
        else:
            config['photometry']['output'] = output

    if config.get('photometry', 'archive_local') == "None" or overwrite:
        if archive_local is None:
            config['photometry']['archive_local'] = input('Enter local data archive directory absolute path:')
        else:
            config['photometry']['archive_local'] = archive_local

    with open(config_file, 'w') as cfgfile:
        config.write(cfgfile)

    clear_config_cache()


def set_tns_token(api_key: Optional[str] = None, filename: str = 'config.ini', overwrite:bool = False) -> None:
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    config = configparser.ConfigParser()
    config.read(config_file)

    if config.get('TNS', 'api_key') == "None" or overwrite:
        if api_key is None:
            config['TNS']['api_key'] = input('Enter photometry output directory absolute path:')
        else:
            config['TNS']['api_key'] = api_key

    with open(config_file, 'w') as cfgfile:
        config.write(cfgfile)

    clear_config_cache()


def create_config(tns:bool = False):
    set_api_token(overwrite=True)
    set_photometry_folders(overwrite=True)
    if tns:
        set_tns_token(overwrite=True)
    clear_config_cache()


def copy_from_other_config(filepath: str, filename: str = 'config.ini'):
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)
    config_sourcefile = os.path.expanduser(filepath)

    config_source = configparser.ConfigParser()
    config_dest= configparser.ConfigParser()

    config_source.read(config_sourcefile)
    config_dest.read(config_file)

    config_dest['api'] = config_source['api']
    config_dest['photometry'] = config_source['photometry']
    config_dest['TNS'] = config_source['TNS']

    with open(config_file, 'w') as cfgfile:
        config_dest.write(cfgfile)
    clear_config_cache()
