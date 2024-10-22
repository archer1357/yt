
import os, pickle, time
from collections import OrderedDict


import sqlite3
import csv
import json, string


# ascii_table=['_' for x in range(0,256)]

# for i in range(0,len(string.printable)):
#     ascii_table[ord(string.printable[i])]=string.printable[i]

def read_csv_file(fn):
    with open(csv_fn, newline='', encoding="utf8") as csvfile:
        spamreader = csv.reader(fn, delimiter=',', quotechar='"')
        return spamreader

def read_json_file(fn):
    with open(fn, mode='r', encoding="utf8") as file: #b
        data = file.read()
        # data = [ord(ascii_table[x]) for x in data]
        # data = json.loads(bytes(data))
        data = json.loads(data)
        return data

def write_channel_csv_to_db(csv_fn, db_fn):
    try:
        conn = sqlite3.connect('test.db')

        with open(csv_fn, newline='', encoding="utf8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in spamreader:

                if len(row) != 0:
                    # print(row[0])


                    cid=row[0]
                    ctitle=row[2]
                    cdate='9999-01-01T00:00:00Z'
                    conn.execute("INSERT INTO channel (id,date,title) VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET date=? WHERE (date=='' OR date>?) AND ?!='';",
                                 (cid,cdate,ctitle,cdate,cdate,cdate))


                    conn.execute("INSERT INTO subscribed (id,date,title) VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET date=? WHERE (date=='' OR date>?) AND ?!='';",
                                 (cid,cdate,ctitle,cdate,cdate,cdate))

                    conn.commit()

    # except Exception as e:
    #    raise e
    finally:
        conn.close()


def write_video_json_to_db(json_fn,db_fn,userChannelId):

    conn = sqlite3.connect('test.db')

    root=read_json_file(json_fn)

    cursor = conn.execute("SELECT id FROM video;")
    dbVideoIds = set([x[0] for x in cursor])

    cursor = conn.execute("SELECT videoid FROM watched WHERE userchannelid=?;",[userChannelId])
    dbWatchedVideoIds = set([x[0] for x in cursor])

    for v in root:
        if 'titleUrl' in v:
            title=v['title'][8:]
            videoId=v['titleUrl'][32:]
            date=v['time']
            channelId=v['subtitles'][0]['url'][32:] if 'subtitles' in v else ''

            if videoId not in dbVideoIds:
                conn.execute("INSERT INTO video (id,title,channelid) VALUES(?,?,?);",(videoId,title,channelId))
                conn.commit()
                # ON CONFLICT(id) DO UPDATE SET date=? WHERE (date=='' OR date>?) AND ?!=''
                #date,'',date,date,date

            if videoId not in dbWatchedVideoIds:
                conn.execute("INSERT INTO watched (userchannelid,videoid,date) VALUES(?,?,?) ON CONFLICT(userchannelid,videoid) DO UPDATE SET date=? WHERE (date=='' OR date>?);",
                             (userChannelId,videoId,date, date,date))

                conn.commit()




            # conn.execute("INSERT INTO video (id,date,title,rating,channelid) VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET date=? WHERE (date=='' OR date>?) AND ?!='';",
            #              (videoId,date,title,'',channelId,date,date,date))

            # conn.commit()


                # cid=row[0]
                # ctitle=row[2]
                # cdate='9999-01-01T00:00:00Z'



    conn.close()

# write_channel_csv_to_db("subscriptions.csv", "test.db")
write_video_json_to_db("watch-history.json", "test.db","YOURCHANNELID")
