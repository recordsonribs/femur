import re
import unicodedata

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

def only_real_files(list):
	return [x for x in list if not x.startswith('.')]

def clean_format(format):
	return 'ogg' if format.endswith('Vorbis') else format.lower()

def truncate(string):
	bits = string.split()

	if len(bits) <= 3:
		return '-'.join(bits)

	return ''.join(word[0] for word in bits)

def remove_special_characters(string):
	return re.sub('[^A-Za-z0-9 \.]+', '', string)

def clean_up_input(string):
	string = strip_accents(string)
	string = remove_special_characters(string)
	string = truncate(string)
	return string.lower()

def zip_file_name(artist, title, format):
	return '-'.join([clean_up_input(artist), clean_up_input(title), clean_format(format)]) + '.zip'

def img_file_name(album, size):
	return '-'.join([album.lower(), (str(size) + 'x' + str(size))]) + '.jpg'

def directory_name(artist, title, format):
	if format.endswith('Vorbis'):
		format = 'Ogg'
	return '%s - %s [%s]' % (artist, title, format)
