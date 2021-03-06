# coding=utf8
from __future__ import absolute_import

import unittest

from femur.utils import (clean_format, strip_accents, zip_file_name,
                         img_file_name, directory_name)


class TestCleanFormat(unittest.TestCase):

    def test_detects_vobris_and_removes(self):
        assert clean_format('Ogg Vorbis') == 'ogg'

    def test_passes_through_other_formats(self):
        assert clean_format('MP3') == 'mp3'


class TestStripAccents(unittest.TestCase):

    def test_strips_accents_we_might_find_a_problem(self):
        assert strip_accents('Les Étoiles über Mère Françoise noël') == \
            'Les Etoiles uber Mere Francoise noel'


class TestZipFileName(unittest.TestCase):

    def test_format_is_lowercased(self):
        assert zip_file_name('a', 'b', 'FLAC') == 'a-b-flac.zip'

    def test_single_word_artist_and_album(self):
        assert zip_file_name('Radiohead', 'Drill', 'MP3') == \
            'radiohead-drill-mp3.zip'

    def test_multiple_word_artist_under_three_words_is_passed_through(self):
        assert zip_file_name('The Smashing Pumpkins', 'Machina', 'FLAC') \
            == 'the-smashing-pumpkins-machina-flac.zip'

    def test_artist_with_artist_over_three_words_is_truncated(self):
        artist = 'All The Empires Of The World'
        assert zip_file_name(artist, 'Album', 'MP3')\
            == 'ateotw-album-mp3.zip'

    def test_multiple_word_title_under_three_words_is_passed_through(self):
        assert zip_file_name('Radiohead', 'OK Computer', 'ogg') == \
            'radiohead-ok-computer-ogg.zip'

    def test_title_with_three_words_is_truncated(self):
        assert zip_file_name('Artist', 'One Two Three Four', 'MP3') == \
            'artist-ottf-mp3.zip'

    def test_artist_with_special_characters_is_stripped(self):
        assert zip_file_name('Artist!?!?%%%&&&@@@!?', 'Album', 'MP3') \
            == 'artist-album-mp3.zip'

    def test_album_with_special_characters_but_short_is_stripped(self):
        assert zip_file_name('Artist', 'Some Short Name?!!', 'MP3') \
            == 'artist-some-short-name-mp3.zip'

    def test_artist_with_foreign_characters_is_handled(self):
        assert zip_file_name('Les Étoiles', 'Album', 'FLAC') \
            == 'les-etoiles-album-flac.zip'

    def test_album_with_foreign_characters_is_handled(self):
        assert zip_file_name('Normal Name', 'über', 'MP3') \
            == 'normal-name-uber-mp3.zip'

    def test_esoteric_records_on_ribs_album_examples(self):
        assert zip_file_name('Blah', 'Going to Jib Choons \
        (Choons for Going to Jib Like Innit)', 'MP3') \
            == 'blah-gtjccfgtjli-mp3.zip'

        a = 'Talk Less Say More'
        f = 'FLAC'
        assert zip_file_name(a, '\'It’s About Time\'', f)\
            == 'tlsm-its-about-time-flac.zip'

        assert zip_file_name('Les Étoiles', 'To Leave A Mark', 'MP3') \
            == 'les-etoiles-tlam-mp3.zip'

        assert zip_file_name('Ga’an', 'Ga’an', 'FLAC')\
            == 'gaan-gaan-flac.zip'

        a = 'All The Empires Of The World'
        assert zip_file_name(a, 'CVRSVS', 'FLAC')\
            == 'ateotw-cvrsvs-flac.zip'


class TestImageFileName(unittest.TestCase):

    def test_image_file_removes_exotic_characters(self):
        assert img_file_name('This! Is! Éxotic!', 300) \
            == 'this-is-exotic-300x300.jpg'

    def test_image_file_truncates_lengthy_album_names(self):
        title = 'really long album name with a lot of stuff going on'
        assert img_file_name(title, 450) == 'rlanwalosgo-450x450.jpg'


class TestDirectoryName(unittest.TestCase):

    def test_directory_name_is_correctly_formatted(self):
        assert directory_name('Les Étoiles', 'Album?!?!', 'Ogg') \
            == 'Les Étoiles - Album?!?! [Ogg]'

    def test_directory_name_includes_very_long_names(self):
        artist = 'Strap The Button'
        title = 'Going to Jib Choons (Choons for Going to Jib Like Innit)'
        assert directory_name(artist, title, 'MP3') == \
            'Strap The Button - {} [MP3]'.format(title)
