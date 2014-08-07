'''Dump the data from the database into JSON files.'''
import dbm
import collections
import json

def main():
    video_2_user_db = dbm.open('video_2_user.dbm', 'r')
    video_2_server_db = dbm.open('video_2_server.dbm', 'r')

    pool = collections.defaultdict(dict)

    with open('video_2_user.csv', 'w', newline='') as video_2_user_file:
        for video in sorted(video_2_user_db.keys()):

            video_id = video.decode()

            if video not in video_2_server_db:
                print('Warning:', video, 'not in database.')
                url = None
            else:
                url = video_2_server_db[video].decode()

            video_id_key = video_id[0:2]
            pool[video_id_key][video_id] = url

    for key, data in pool.items():
        with open('data-{}.json'.format(key), 'w') as out_file:
            out_file.write(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
