'''Add supplemental info from ArchiveTeam CSV manifest to database.'''
import dbm
import csv


def main():
    video_2_user_db = dbm.open('video_2_user.dbm', 'c')
    video_2_server_db = dbm.open('video_2_server.dbm', 'c')

    with open('justout.csv', 'r', newline='') as in_file:
        reader = csv.reader(in_file, delimiter=';')

        for row in reader:
            video_id = row[0]
            url = row[7]
            print(video_id, url)
            video_2_server_db[video_id] = url

    video_2_user_db.close()
    video_2_server_db.close()


if __name__ == '__main__':
    main()
