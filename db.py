import glob, os, bs4, re, sys, time
import sqlite3
import csv, json, string


sys.path.append("..")

import yt
def ReadChannelsFile(fn):

    #id,date,title
    with open(fn,mode='w') as file:
        lines=file.read().splitlines()

def WriteChannelsFile(service,fn):
    ""
    with open(fn,mode='w') as file:
        ""

def GetReadWriteChannels(service,fn):
    ""



def GetReadWriteRatedVideos(service,fn):
    ""
    #id,date,channel_index,title

def StoreChannelInDB(channelId,channelTitle, conn=None):
    conn = conn if conn != None else sqlite3.connect('test.db')
    conn.execute("INSERT OR IGNORE INTO channel (id,title) VALUES(?,?);",[channelId,channelTitle])
    conn.commit()

def StoreVideoInDB(videoId,videoTitle,videoUploadDate,channelId, conn=None):
    conn = conn if conn != None else sqlite3.connect('test.db')

    cursor = conn.execute("INSERT OR IGNORE INTO video (id,date,title,channelid) VALUES (?,?,?,?);",
                          [videoId,videoUploadDate,videoTitle,channelId])
    conn.commit()

def GetStoreLikedVideosInDB(service):

    userChannelId=GetMyChannelId(service)
    print(userChannelId)
    conn = sqlite3.connect('test.db')

    # myPlaylists=GetMyPlaylistTitlesAndIdsDict(service)

    # for k,v in myPlaylists.items():
    #     print('{} : {}'.format(k,v))



    ratedVideos=GetAllMyRatedVideos(service)
    print(len(ratedVideos))

    for v in ratedVideos:
        videoId=v['videoId']
        videoTitle=v['videoTitle']
        rating=v['rating']
        date=v['date']
        channelId=v['channelId']
        channelTitle=v['channelTitle']

        # print( [videoId,videoTitle,channelId])


        cursor = conn.execute("SELECT * FROM rating WHERE userchannelid=? AND videoid=?;", [userChannelId,videoId])
        if len([x for x in cursor]) ==0:
            print([videoId,channelId,date])

        StoreVideoInDB(videoId,videoTitle,'',channelId, conn)
        StoreChannelInDB(channelId,channelTitle, conn)
        # cursor = conn.execute("INSERT OR IGNORE INTO video (id,date,title,channelid) VALUES (?,'',?,?);",
        #                       [videoId,videoTitle,channelId])
        # cursor = conn.execute("INSERT OR IGNORE INTO channel (id,title) VALUES (?,?);",
        #                       [channelId,channelTitle])
        cursor = conn.execute("INSERT OR IGNORE INTO rating (userchannelid,videoid,rating,date) VALUES (?,?,?,?);",
                              [userChannelId,videoId,rating,date])

        cursor = conn.execute("UPDATE rating SET date=? WHERE (date='' OR date>?) AND videoid=? AND userchannelid=?;",
                              [date,date,videoId,userChannelId])
        #
        # cursor = conn.execute("INSERT OR IGNORE INTO rating (userchannelid,videoid,rating,date) VALUES (?,?,?,?);",
        #                       [userChannelId,videoId,rating,date])
        conn.commit()


    conn.close()



def GetStoreVideoRatingsInDB(service):

    userChannelId=GetMyChannelId(service)
    print(userChannelId)
    conn = sqlite3.connect('test.db')



    cursor = conn.execute("SELECT video.id FROM video WHERE id NOT IN (SELECT videoid FROM rating WHERE userchannelid==?);",
                          [userChannelId])
    videoIds= [x[0] for x in cursor]
    print(len(videoIds))

    n=50
    for x in range(0,(len(videoIds)+n-1)//n):
        startInd=x*n
        endInd=min((x+1)*n,len(videoIds))

        print("x={}, {}-{}".format(x,startInd,endInd))
        ratings=GetVideoRatings(service,videoIds[startInd:endInd])

        for i,rating in enumerate(ratings):

            conn.execute("INSERT INTO rating (userchannelid,videoid,rating) VALUES(?,?,?);",
                         (userChannelId,videoIds[startInd+i],rating))
        conn.commit()

    # print(channelIds)
    # for row in cursor:
    #     print(row)

    conn.close()

def GetStoreSubsribedInDB(service):
    ""



def GetStoreChannelsSubsInDB(service):
    userChannelId=GetMyChannelId(service)
    subs=GetChannelSubsInfo(service,userChannelId)

    print(len(subs))

    conn = sqlite3.connect('test.db')



    cursor = conn.execute("SELECT channel.id FROM channel;")
    # dbChannels = set([x[0] for x in cursor])


    cursor = conn.execute("SELECT channelid FROM subscribed WHERE userchannelid=?;", [userChannelId])
    dbSubs = set([x[0] for x in cursor])


    for sub in subs:
        channelId=sub[0]
        date=sub[1]
        title=sub[2]

        StoreChannelInDB(channelId,title, conn)

        # dbChannels.add(channelId)

        if channelId not in dbSubs:
            # print("{} {} {}".format(userChannelId,channelId,date))
            conn.execute("INSERT INTO subscribed (userchannelid,channelid,date) VALUES(?,?,?);",[userChannelId,channelId,date])
            conn.commit()
            dbSubs.add(channelId)



            # ON CONFLICT(userchannelid,channelid) DO UPDATE SET date=? WHERE (date=='' OR date>?) AND ?!=''
            #, cdate,cdate,cdate





    # print("{} {}".format(len(dbChannels),len(dbSubs)))

    # cursor = conn.execute("SELECT id, title, date FROM channel")
    # for row in cursor:
    #     print(row)
    conn.close()



def GetMyPlaylistIds(service):
    items=yt.GetList(service.playlists(), {'part':'contentDetails','mine':True})
    return [x['id'] for x in items]


def GetPlaylistVideoInfos(service,playlistId):
    items=yt.GetList(service.playlistItems(), {'part':'snippet','playlistId':playlistId})
    return [{
        'videoId' : x['id'],
        'videoTitle' : x['snippet']['title'],
        'channelId' : x['snippet']['channelId'],
        'channelTitle' : x['snippet']['channelTitle'],
        'publishedAt' : x['snippet']['publishedAt']
    } for x in items]

def GetMyChannelId(service):
    items = yt.GetList(service.channels(), {'part':'snippet','mine':True})
    return items[0]['id']

def GetAllMyRatedVideos(service):
    like_items = yt.GetList(service.videos(), {'part':"snippet", 'myRating':'like'})
    dislike_items=yt.GetList(service.videos(), {'part':"snippet", 'myRating':'dislike'})

    for x in like_items:
        x['rating']='like'

    for x in dislike_items:
        x['rating']='dislike'

    all_items=like_items+dislike_items

    return [{
        'videoId':x['id'],
        'videoTitle':x['snippet']['title'],
        'date':x['snippet']['publishedAt'],
        'rating':x['rating'],
        'channelId':x['snippet']['channelId'],
        'channelTitle':x['snippet']['channelTitle']
    } for x in all_items]

def GetStorePlaylistVideosInDB(service):

    playlistIds=GetMyPlaylistIds(service)
    videoInfos=[GetPlaylistVideoInfos(service,playlistId) for playlistId in playlistIds]
    videoInfos=[y for x in videoInfos for y in x ]


    for videoInfo in videoInfos:
        print("{} {}".format(videoInfo['videoId'],videoInfo['videoTitle']))
        StoreVideoInDB(videoInfo['videoId'],videoInfo['videoTitle'],videoInfo['publishedAt'],videoInfo['channelId'])
        StoreChannelInDB(videoInfo['channelId'],videoInfo['channelTitle'])


service = yt.Create_Service2('a','..')
print(service)

print(GetMyChannelId(service))
GetStoreLikedVideosInDB(service)


GetStorePlaylistVideosInDB(service)

service = yt.Create_Service2('b','..')
print(service)

print(GetMyChannelId(service))
GetStoreLikedVideosInDB(service)
GetStorePlaylistVideosInDB(service)

##########################
# GetStoreChannelsSubsInDB(service)
# GetStoreVideoRatingsInDB(service)

#

# print(GetMyChannelId(service))
