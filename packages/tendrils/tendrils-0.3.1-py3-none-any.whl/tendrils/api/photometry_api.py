"""
Upload photometry results to Flows server.
"""

import glob
import logging
import os
import shutil
import zipfile
import tempfile
from typing import Union, Optional
from configparser import ConfigParser
from astropy.table import Table
from tqdm import tqdm

from tendrils.api import get_datafile
from tendrils.utils import get_api_token, get_request, load_config, get_filehash, post_request, URLS


def get_photcache(config: Optional[ConfigParser] = None) -> tuple[str, Optional[tempfile.TemporaryDirectory]]:
    """
    Get photometry cache from config or create a temporary one
    Args:
        config: ConfigParser instance with 'api' and 'photometry_cache' defined.

    Returns: tuple[str, str]: tuple (photcache path, reference to tmpdir).
     If photometry_cache was supplied via config, the latter is None.
    """
    # Use config if given:
    if config is not None:
        photcache = config.get('api', 'photometry_cache', fallback=None)
    else:
        photcache = None

    # Try config location if exists, default to tempdir if not valid:
    tmpdir = None
    if photcache is not None:
        photcache = os.path.abspath(photcache)
        if not os.path.isdir(photcache):
            raise FileNotFoundError(f"Photometry cache directory does not exist: {photcache}")
    else:
        tmpdir = tempfile.TemporaryDirectory(prefix='flows-api-get_photometry-')
        photcache = tmpdir.name

    return photcache, tmpdir


def create_photdir(config: ConfigParser,
                   target_name: str,
                   fileid: Union[int, str]) -> str:
    """
    Get photdir for given fileid and target_name
    Args:
        fileid (int, str): fileid
        target_name (str): target_name
        config (configparser.ConfigParser): current config instance
    Returns: photdir: absolute path to photdir.

    """
    fileid_str = f'{int(fileid):05d}'
    photdir_root = config.get('photometry', 'output', fallback='.')

    # Find the photometry output directory for this fileid:
    photdir = os.path.join(photdir_root, target_name, fileid_str)
    if not os.path.isdir(photdir):
        # Do a last check, to ensure that we have not just added the wrong number of zeros
        # to the directory name:
        found_photdir = []
        for d in os.listdir(os.path.join(photdir_root, target_name)):
            if d.isdigit() and int(d) == fileid and os.path.isdir(d):
                found_photdir.append(os.path.join(photdir_root, target_name, d))
        # If we only found one, use it, otherwise throw an exception:
        if len(found_photdir) == 1:
            photdir = found_photdir[0]
        elif len(found_photdir) > 1:
            raise RuntimeError(f"Several photometry output found for fileid={fileid}. \
                    You need to do a cleanup of the photometry output directories.")
        else:
            raise FileNotFoundError(photdir)

    photdir = os.path.abspath(photdir)
    return photdir


def make_zip(files: list, fileid: Union[int, str], current_dir: Union[tempfile.TemporaryDirectory, str]):
    # Logging and tqdm
    logger = logging.getLogger(__name__)
    tqdm_settings = {'disable': None if logger.isEnabledFor(logging.INFO) else True}

    # Create ZIP-file within the temp directory:
    fpath_zip = os.path.join(current_dir, f'{int(fileid):05d}.zip')

    # Create ZIP file with all the files:
    with zipfile.ZipFile(fpath_zip, 'w', allowZip64=True) as z:
        for f in tqdm(files, desc=f'Zipping {int(fileid):d}', **tqdm_settings):
            logger.debug('Zipping %s', f)
            z.write(f, os.path.basename(f))

    # Change the name of the uploaded file to contain the file hash:
    fhash = get_filehash(fpath_zip)
    fname_zip = f'{int(fileid):05d}-{fhash:s}.zip'

    return fhash, fname_zip


def get_photometry(photid: int) -> Table:
    """
    Retrieve lightcurve from Flows server.

    Please note that it can significantly speed up repeated calls to this function
    to specify a cache directory in the config-file under api -> photometry_cache.
    This will download the files only once and store them in this local cache for
    use in subsequent calls.

    Parameters:
        photid (int): Fileid for the photometry file.

    Returns:
        :class:`astropy.table.Table`: Table containing photometry.
    """
    token = get_api_token()
    config = load_config()
    photcache, tmpdir = get_photcache(config)

    # Construct path to the photometry file in the cache:
    photfile = os.path.join(photcache, f'photometry-{photid:d}.ecsv')

    if not os.path.isfile(photfile):
        # Send query to the Flows API:
        params = {'fileid': photid}
        r = get_request(URLS.photometry_url, token=token, params=params)

        # Create temporary directory and save the file into there,
        # then open the file as a Table:
        with open(photfile, 'w') as fid:
            fid.write(r.text)

    # Read the photometry file:
    tab = Table.read(photfile, format='ascii.ecsv')

    # Explicitly cleanup the temporary directory if it was created:
    if tmpdir:
        tmpdir.cleanup()

    return tab


def upload_photometry(fileid: Union[int, str], delete_completed: bool = False) -> None:
    """
    Upload photometry results to Flows server.

    This will make the uploaded photometry the active/newest/best photometry and
    be used in plots and shown on the website.

    Parameters:
        fileid: [int, str]: File ID of photometry to upload to server.
        delete_completed: bool, optional: Delete the photometry from the local
            working directory if the upload was successful. Default=False.
    """

    logger = logging.getLogger(__name__)

    # Use API to get the datafile information:
    datafile = get_datafile(fileid)
    token = get_api_token()
    config = load_config()
    photdir = create_photdir(config, datafile['target_name'], fileid)

    # Make sure required files are actually there:
    files_existing = os.listdir(photdir)
    if 'photometry.ecsv' not in files_existing:
        raise FileNotFoundError(os.path.join(photdir, 'photometry.ecsv'))
    if 'photometry.log' not in files_existing:
        raise FileNotFoundError(os.path.join(photdir, 'photometry.log'))

    # Create list of files to be uploaded:
    files = [os.path.join(photdir, 'photometry.ecsv'), os.path.join(photdir, 'photometry.log')]
    files += glob.glob(os.path.join(photdir, '*.png'))

    # Create ZIP file:
    with tempfile.TemporaryDirectory(prefix='flows-upload-') as tmpdir:
        # Create ZIP-file within the temp directory:
        fhash, fname_zip = make_zip(files, fileid, tmpdir)
        fpath_zip = os.path.join(tmpdir, f'{fileid:05d}.zip')

        # Send file to the API:
        logger.info("Uploading to server...")
        with open(fpath_zip, 'rb') as fid:
            r = post_request(URLS.photometry_upload_url, token=token, params={'fileid': fileid},
                             files={'file': (fname_zip, fid, 'application/zip')})

    # Check the returned data from the API:
    if r.text.strip() != 'OK':
        logger.error(r.text)
        raise RuntimeError("An error occurred while uploading photometry: " + r.text)

    # If we have made it this far, the upload must have been a success:
    if delete_completed:
        if set([os.path.basename(f) for f in files]) == set(os.listdir(photdir)):
            logger.info("Deleting photometry from workdir: '%s'", photdir)
            shutil.rmtree(photdir, ignore_errors=True)
        else:
            logger.warning("Not deleting photometry from workdir: '%s'", photdir)
