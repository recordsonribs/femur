import femur.utils as utils

class TestCleanFormat:

    def test_detects_vobris_and_removes(self):
        assert utils.clean_format('Ogg Vorbis') == 'Ogg'

    def test_passes_through_other_formats(self):
        assert utils.clean_format('MP3 Magic Time') == 'MP3 Magic Time'


class TestZipFileName:

    def test_current_functionality(self):
        assert utils.zip_file_name('Artist', 'Title', 'FLAC') == 'a-title-flac.zip'
