def only_real_files(list):
	return [x for x in list if not x.startswith('.')]

def clean_format(format):
	return 'Ogg' if format.endswith('Vorbis') else format

def zip_file_name(artist, title, format):
	return "-".join(["".join(word[0].lower() for word in artist.split()), title.lower(), clean_format(format).lower()]) + ".zip"

def img_file_name(album, size):
	return "-".join([album.lower(), (str(size) + 'x' + str(size))]) + '.jpg'

def directory_name(artist, title, format):
	if format.endswith('Vorbis'):
		format = 'Ogg'
	return "%s - %s [%s]" % (artist, title, format)