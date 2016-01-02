import os

from femur.utils import only_real_files
from mutagen.flac import FLAC


def get_info_from_flacs(directory):
    """Returns artist and album name by reading a FLAC file.

    Args:
        directory (string): Directory to look for FLAC files in to read

    Returns:
        tuple: Tuple of artist and album title.
    """
    flac_dir = os.path.join(directory, 'FLAC')

    if not os.path.isdir(flac_dir):
        raise FLACReadError(
            '{} is not a directory containg FLAC files'.format(flac_dir)
        )

    flacs = only_real_files(os.listdir(flac_dir))

    audio = FLAC(os.path.join(flac_dir, flacs[0]))
    return audio['artist'][0], audio['album'][0]


class FLACReadError(Exception):
    pass
