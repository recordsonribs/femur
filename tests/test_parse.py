import femur.parse as parse

import unittest
import pytest
from mock import patch, call


class TestImageFileName(unittest.TestCase):

    @patch('femur.parse.os.path.isdir', return_value=False)
    def test_file_is_checked(self, mock_path):
        with pytest.raises(parse.FLACReadError) as excinfo:
            parse.get_info_from_flacs('/some/path')

        assert mock_path.call_args == call('/some/path/FLAC')
        assert '/some/path/FLAC is not a directory containg FLAC files'\
            == str(excinfo.value)

    @patch('femur.parse.os.path.isdir', return_value=True)
    @patch('femur.parse.os.listdir', return_value=['..', '01 Song.flac'])
    @patch('femur.parse.FLAC')
    def test_method_works(self, mock_flac, mock_list_dir, mock_path):
        mock_flac.return_value = {
            'artist': ['Test Artist'],
            'album': ['Test Release']
        }

        artist, release = parse.get_info_from_flacs('/some/path')
        assert mock_path.call_args_list[0] == call('/some/path/FLAC')
        assert mock_path.called is True

        assert mock_list_dir.called is True
        assert mock_list_dir.call_args == call('/some/path/FLAC')

        assert mock_flac.called is True
        assert mock_flac.call_args == call('/some/path/FLAC/01 Song.flac')

        assert artist == 'Test Artist'
        assert release == 'Test Release'
