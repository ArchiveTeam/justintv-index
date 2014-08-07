'''Script to grab all the CDX files.'''
import os.path
import requests
import re


def main():
    response = requests.get('https://archive.org/advancedsearch.php?q=collection%3Ajustintv&fl%5B%5D=identifier&sort%5B%5D=addeddate+asc&sort%5B%5D=&sort%5B%5D=&rows=500&page=1&output=json&save=yes')

    doc = response.json()
    rows = doc['response']['docs']
    identifiers = list([row['identifier'] for row in rows])

    assert len(identifiers) < 500

    for identifier in identifiers:
        filename = '{}.megawarc.warc.os.cdx.gz'.format(identifier)

        if os.path.exists(filename):
            continue

        print('Fetching', identifier)
        url = 'https://archive.org/download/{}/justintv_{}.megawarc.warc.os.cdx.gz'.format(
            identifier,
            re.search(r'_([\d]{8,})', identifier).group(1)
        )

        print(url)
        response = requests.get(url)

        assert response.status_code == 200

        temp_filename = filename + '-tmp'
        with open(temp_filename, 'wb') as out_file:
            out_file.write(response.content)

        os.rename(temp_filename, filename)



if __name__ == '__main__':
    main()
