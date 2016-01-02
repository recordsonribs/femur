# coding=utf8
import femur.utils as utils

class TestCleanFormat:

    def test_detects_vobris_and_removes(self):
        assert utils.clean_format('Ogg Vorbis') == 'ogg'

    def test_passes_through_other_formats(self):
        assert utils.clean_format('MP3') == 'mp3'


class TestStripAccents:

    def test_strips_accents_we_might_find_a_problem(self):
        assert utils.strip_accents('Les Étoiles über Mère Françoise noël') == 'Les Etoiles uber Mere Francoise noel'


class TestZipFileName:

    def test_format_is_lowercased(self):
        assert utils.zip_file_name('a', 'b', 'FLAC') == 'a-b-flac.zip'

    def test_single_word_artist_and_album(self):
        assert utils.zip_file_name('Radiohead', 'Drill', 'MP3') == 'radiohead-drill-mp3.zip'

    def test_multiple_word_artist_under_three_words_is_passed_through(self):
        assert utils.zip_file_name('The Smashing Pumpkins', 'Machina', 'FLAC') == 'the-smashing-pumpkins-machina-flac.zip'

    def test_artist_with_artist_over_three_words_is_truncated(self):
        assert utils.zip_file_name('All The Empires Of The World', 'Album', 'MP3') == 'ateotw-album-mp3.zip'

    def test_multiple_word_title_under_three_words_is_passed_through(self):
        assert utils.zip_file_name('Radiohead', 'OK Computer', 'ogg') == 'radiohead-ok-computer-ogg.zip'

    def test_title_with_three_words_is_truncated(self):
        assert utils.zip_file_name('Artist', 'One Two Three Four', 'MP3') == 'artist-ottf-mp3.zip'

    def test_artist_with_special_characters_is_stripped(self):
        assert utils.zip_file_name('Artist!?!?%%%&&&@@@!?', 'Album', 'MP3') == 'artist-album-mp3.zip'

    def test_album_with_special_characters_but_short_is_stripped(self):
        assert utils.zip_file_name('Artist', 'Some Short Name?!!', 'MP3') == 'artist-some-short-name-mp3.zip'

    def test_artist_with_foreign_characters_is_handled(self):
        assert utils.zip_file_name('Les Étoiles', 'Album', 'FLAC') == 'les-etoiles-album-flac.zip'

    def test_album_with_foreign_characters_is_handled(self):
        assert utils.zip_file_name('Normal Name', 'über', 'MP3') == 'normal-name-uber-mp3.zip'

    def test_esoteric_records_on_ribs_album_examples(self):
        assert utils.zip_file_name('Blah', 'Going to Jib Choons (Choons for Going to Jib Like Innit)', 'MP3') == 'blah-gtjccfgtjli-mp3.zip'
        assert utils.zip_file_name('Talk Less Say More', '\'It’s About Time\'', 'Flac') == 'tlsm-its-about-time-flac.zip'
        assert utils.zip_file_name('Les Étoiles', 'To Leave A Mark', 'MP3') == 'les-etoiles-tlam-mp3.zip'
        assert utils.zip_file_name('Ga’an', 'Ga’an', 'FLAC') == 'gaan-gaan-flac.zip'
        assert utils.zip_file_name('All The Empires Of The World', 'CVRSVS', 'FLAC') == 'ateotw-cvrsvs-flac.zip'
