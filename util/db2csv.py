'''Dump the data from the database into CSV files.'''
import dbm
import csv


def main():
    video_2_user_db = dbm.open('video_2_user.dbm', 'r')
    video_2_server_db = dbm.open('video_2_server.dbm', 'r')

    with open('video_2_user.csv', 'w', newline='') as video_2_user_file:
        writer = csv.writer(video_2_user_file)
        writer.writerow(['Video ID', 'Username'])

        for video in sorted(video_2_user_db.keys()):
            writer.writerow([video.decode(), video_2_user_db[video].decode()])

    with open('video_2_server.csv', 'w', newline='') as video_2_server_file:
        writer = csv.writer(video_2_server_file)
        writer.writerow(['Video ID', 'Server Media URL'])

        for video in sorted(video_2_server_db.keys()):
            if video not in video_2_user_db:
                print('Warning: ', video, 'not in database skipping.')
                continue

            writer.writerow([video.decode(), video_2_server_db[video].decode()])


if __name__ == '__main__':
    main()
