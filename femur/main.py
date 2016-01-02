# coding=utf-8
import sys
import os
import yaml

import femur.utils as utils


def main():
    if len(sys.argv) < 2:
        print "Usage:"
        print "femur <directory to load audio files from>"
        sys.exit(1)

    if not os.path.isfile('./config.yaml'):
        print "Please set up a config.yaml file in this directory."
        sys.exit(1)

    config = yaml.load(open('config.yaml', 'r'))

    directory = sys.argv[1]

    if os.path.isdir(directory) is False:
        print "%s is not a directory." % directory
        sys.exit(1)

    files = os.listdir(directory)

    if any('FLAC' in item for item in files) is True:
        print "Couldn't find FLAC directory in %s" % directory
        print "We need this to work some things out."
        sys.exit(1)

    flac_dir = os.path.join(directory, 'FLAC')
    flacs = utils.only_real_files(os.listdir(flac_dir))

    from mutagen.flac import FLAC

    audio = FLAC(os.path.join(flac_dir, flacs[0]))
    artist = unicode(audio["artist"][0])
    album = unicode(audio["album"][0])

    print "Reading %s - %s for release." % (artist, album)

    import zipfile
    import tinys3
    from progressbar import ProgressBar
    from PIL import Image

    s3_config = config["s3"]
    conn = tinys3.Connection(
        s3_config["access_key"],
        s3_config["secret_key"],
        endpoint="s3-eu-west-1.amazonaws.com"
    )

    artwork_location = os.path.join(directory, 'FLAC', 'Artwork.jpg')
    thumbnail_location = directory

    if not os.path.exists(artwork_location):
        print "Artwork not found, please place the artwork as JPEG at %s"\
            % artwork_location
        sys.exit(1)

    im = Image.open(artwork_location)

    print "Uploading artwork."

    print "Creating thumbnails."
    for size in [130, 308]:
        i = im.resize((size, size), Image.ANTIALIAS)
        image_file = utils.img_file_name(album, size)
        img_file_location = os.path.join(thumbnail_location, image_file)

        i.save(img_file_location, "JPEG", quality=100)

        print "Uploading image %s to S3." % image_file
        f = open(img_file_location, 'rb')

        if size == 130:
            size_name = 'tiny'
        else:
            size_name = 'large'

        # This is for legacy reasons we name all our files on the server
        # using directories to work out what they are.
        conn.upload("/".join(
            [size_name, album.lower() + '.jpg']),
            f,
            s3_config["artwork_bucket"]
        )
        f.close()

    print "Uploading full size artwork."
    f = open(artwork_location, 'rb')
    conn.upload(
        "/".join(["huge", album.lower(), ".jpg"]),
        f,
        s3_config["artwork_bucket"]
    )

    f.close()

    # Our Amazon buckets are in different region so :(
    conn = tinys3.Connection(s3_config["access_key"], s3_config["secret_key"])

    # Permitted directories output by Max
    extensions = ('FLAC', 'MP3', 'Vorbis')

    for d in files:
        full_path = os.path.join(directory, d)

        if not d.startswith('.') and os.path.isdir(full_path) \
           and d.endswith(extensions):
            new_name = utils.directory_name(artist, album, d)
            zip_file = utils.zip_file_name(artist, album, d)

            print "Renaming directory from %s to %s" % (d, new_name)
            os.rename(full_path, os.path.join(directory, new_name))
            full_path = os.path.join(directory, new_name)

            print "Zipping %s into file named %s" % (new_name, zip_file)
            zip = zipfile.ZipFile(
                os.path.join(directory, zip_file),
                'w',
                zipfile.ZIP_DEFLATED
            )
            audio_files = os.listdir(full_path)

            pbar = ProgressBar(maxval=len(audio_files)).start()

            i = 0
            for f in audio_files:
                if f.startswith('.'):
                    continue
                zip.write(
                    os.path.join(full_path, f),
                    arcname=os.path.join(new_name, f)
                )
                pbar.update(i + 1)
                i += 1
            zip.close()
            pbar.finish()

            print "Uploading to S3, hold on this could take some time."
            f = open(os.path.join(directory, zip_file), 'rb')
            conn.upload(zip_file, f, s3_config["releases_bucket"])
            f.close()

    print "All done!"

if __name__ == "__main__":
    main()
