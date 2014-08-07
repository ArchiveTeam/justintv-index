'''Process the CDX files into a database.'''
import gzip
import argparse
import dbm
import re


def read_cdx(filename):
    with gzip.open(filename, 'rt') as in_file:
        header = in_file.readline()

        assert header.rstrip() == ' CDX N b a m s k r M S V g'

        for line in in_file:
            (massaged_url, date, url, mime_type, status_code,
            sha1_checksum, redirect, aif_meta_tags, compressed_archive_size,
            archive_offset, filename) = line.rstrip().split()

            yield (massaged_url, date, url, mime_type, status_code,
            sha1_checksum, redirect, aif_meta_tags, compressed_archive_size,
            archive_offset, filename)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('cdx_file', nargs='+')
    args = arg_parser.parse_args()

    video_2_user_db = dbm.open('video_2_user.dbm', 'c')
    video_2_server_db = dbm.open('video_2_server.dbm', 'c')

    for cdx_file in args.cdx_file:
        print('Opening', cdx_file)

        for row in read_cdx(cdx_file):
            (massaged_url, date, url, mime_type, status_code,
            sha1_checksum, redirect, aif_meta_tags, compressed_archive_size,
            archive_offset, filename) = row

            match = re.search(r'justin\.tv/([^/]+)/\w/([\d]+)', url)

            if match:
                user = match.group(1)
                video_id = match.group(2)
                print(video_id, user)
                video_2_user_db[video_id] = user

            match = re.search(r'store.+_([\d]+)\.', url)

            if match:
                video_id = match.group(1)
                print(video_id, url)
                video_2_server_db[video_id] = url

    video_2_user_db.close()
    video_2_server_db.close()


if __name__ == '__main__':
    main()
