"""
Utility functions for dealing with files.
"""
import hashlib


def get_filehash(filename: str):
    """
    Calculate SHA1-hash of file. Raise exception if length is invalid.
    Args:
        filename: str = filename
    Returns: sha1sum file hash
    """
    buf = 65536
    s = hashlib.sha1()
    with open(filename, 'rb') as fid:
        while True:
            data = fid.read(buf)
            if not data:
                break
            s.update(data)

    sha1sum = s.hexdigest().lower()
    if len(sha1sum) != 40:
        raise Exception("Invalid file hash")
    return sha1sum
