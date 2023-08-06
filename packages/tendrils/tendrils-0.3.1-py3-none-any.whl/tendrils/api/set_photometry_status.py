"""
Set photometry status
"""

import logging
from tendrils.utils import get_api_token, get_request, URLS, load_config


def is_pipeline():
    logger = logging.getLogger(__name__)
    # Get API token from config file:
    config = load_config()
    i_am_pipeline = config.getboolean('api', 'pipeline', fallback=False)
    if not i_am_pipeline:
        logger.debug("Not setting status since user is not pipeline")
        return False
    return True


def set_photometry_status(fileid: int, status: str) -> bool:
    """
    Set photometry status.

    Parameters:
        fileid (int):
        status (str): Choices are 'running', 'error' or 'done'.

    .. codeauthor:: Rasmus Handberg <rasmush@phys.au.dk>
    """
    # Validate the input:
    if status not in ('running', 'error', 'abort', 'ingest', 'done'):
        raise ValueError('Invalid status')

    if not is_pipeline():
        return False

    # Get API token from config file:
    token = get_api_token()

    # Send HTTP request to FLOWS server:
    r = get_request(URLS.set_photometry_status_url, token=token, params={'fileid': fileid, 'status': status})
    result = r.text.strip()
    if result != 'OK':
        raise RuntimeError(result)

    return True


def cleanup_photometry_status() -> bool:
    """
    Perform a cleanup of the photometry status indicator.

    This will change all processes still marked as "running"
    to "abort" if they have been running for more than a day.
    """
    # Exit if I am not the pipeline
    if not is_pipeline():
        return False

    # Get API token from config file:
    token = get_api_token()

    # Send HTTP request to FLOWS server:
    r = get_request(URLS.cleanup_photometry_status_url, token=token)
    result = r.text.strip()
    if result != 'OK':
        raise RuntimeError(result)

    return True
