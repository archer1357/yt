def GetChannelSubsInfo(service,userChannelId):
    nextPageToken = None
    subs=[]

    while True:
        time.sleep(request_delay)

        request = service.subscriptions().list(
            part="snippet,contentDetails",
            channelId=userChannelId,
            maxResults=50,
            # order="SUBSCRIPTION_ORDER_RELEVANCE",
            # order="alphabetical",
            # order="relevance",
            # order="unread",
            # mySubscribers=True,
            # mine=True,
            pageToken=nextPageToken
        )

        response = request.execute()
        nextPageToken = response.get('nextPageToken')

        for x in response['items']:
            cid=x['snippet']['resourceId']['channelId']
            ctitle=x['snippet']['title']
            cdate=x['snippet']['publishedAt']
            subs.append([cid,ctitle,cdate])

        if nextPageToken==None:
            break

    return subs
    
def GetMyPlaylistIds(service):
    playlistIds=[]
    nextPageToken = None

    while True:
        time.sleep(request_delay)
        request = service.playlists().list(
            part="contentDetails",
            maxResults=50,
            mine=True,
            pageToken=nextPageToken
        )

        response = request.execute()
        time.sleep(request_delay)
        nextPageToken = response.get('nextPageToken')
        playlistIds.extend([x['id'] for x in response['items']])

        if nextPageToken==None:
            break

    return playlistIds
def GetMyChannelId(service):
    request = service.channels().list(
        part="snippet",
        mine=True
    )
    response = request.execute()
    return response['items'][0]['id']


def GetAllMyRatedVideos(service,rating='like'):
    results=[]
    nextPageToken = None

    while True:
        time.sleep(request_delay)
        request = service.videos().list(
            part="snippet",
            maxResults=50,
            myRating=rating,
            pageToken=nextPageToken
        )
        response = request.execute()

        for x in response['items']:
            results.append({
                'videoId':x['id'],
                'videoTitle':x['snippet']['title'],
                'date':x['snippet']['publishedAt'],
                'rating':rating,
                'channelId':x['snippet']['channelId'],
                'channelTitle':x['snippet']['channelTitle']
            })

        time.sleep(request_delay)
        nextPageToken = response.get('nextPageToken')
        # print('{} {} {}'.format(len(results),len(response['items']),nextPageToken))


        if nextPageToken==None:
            break

    return results



# service = Create_Service(client_secret_file, 'a')
# service = Create_Service(client_secret_file, 'b')
# service = Create_Service(client_secret_file, 'bg')
##########################
# print(GetVideoCount(service,"CHANNELID"))

##########################

# with open('sub2/out.txt') as file:
#     channelIds = file.readlines()
#     channelIds = [line.rstrip() for line in channelIds]
# SubscribeChannels(service, channelIds)
# for c in channelIds:
#     print(c)

##########################
# GetStoreChannelsSubsInDB(service)
# GetStoreVideoRatingsInDB(service)

# GetStoreLikedVideosInDB(service)

# print(GetMyChannelId(service))
##########################


##############################



##########################

# myPlaylistDict=GetMyPlaylistTitlesAndIdsDict(service)
# removePlaylistIds=[myPlaylistDict[x] for x in ['crusaderhist2']]
# removeFromMyPlaylistId=myPlaylistDict['crusaderhist']
# RemovePlaylistsVideosFromMyPlaylist(service,removePlaylistIds,removeFromMyPlaylistId)

##########################
# playlistId='PLAYLISTID'
# ratedVideos=GetPlaylistRatedVideoIdsAndTitles(service,playlistId)

# for x in ratedVideos:
#     print(x)

##########################

# playlistIds=GetMyPlaylistIds(service)
# # videoIds=GetPlaylistsVideoIds(service,playlistIds)
# # videoIds=GetDuplicateVideoIds(service,playlistIds)
# videoIds=GetPlaylistsRatedVideoIds(service,playlistIds)

# # videoIds=list(set(videoIds))

# # print(videoIds)
# for x in videoIds:
#     print(x)

# myPlaylistId=GetOrCreateMyPlaylistId(service,"dups")
# print("myPlaylistId {}".format(myPlaylistId))
# AddNonDuplVideosToPlaylist(service,videoIds,myPlaylistId)

##########################

# myPlaylistId=GetOrCreateMyPlaylistId(service,"dups")
# print("myPlaylistId {}".format(myPlaylistId))

# videoIds=[]
# AddNonDuplVideosToPlaylist(service,videoIds,myPlaylistId)

##########################
# videoIds=[]
# ratings=GetVideoRatings(service,videoIds)
# outVidIds=[v for i,v in enumerate(videoIds) if ratings[i]!='none']
# print(outVidIds)
##########################

# playlistId='PLAYLISTID'
# vids =GetPlaylistUnratedVideoIdsAndTitles(service,playlistId)
# for x in vids:
#     print(x)

# GetPlaylistVideoItems(service,playlistId)

# videoTitlesAndChannelIds=GetVideoTitlesAndChannelIds(service,outVideoIds)

# playlistId='PLAYLISTID'

# videoIds=GetPlaylistVideoIds(service,playlistId)
# for x in videoIds:
#     print(x)

# videoIdsAndTitles=GetPlaylistVideoIdsAndTitles(service,playlistId)
# videoRatings=GetVideoRatings(service,[x[0] for x in videoIdsAndTitles])
# for i,x in enumerate(videoIdsAndTitles):
#     print("{} {} '{}'".format(videoIdsAndTitles[i][0],videoRatings[i],videoIdsAndTitles[i][1]))

# result = GetAllMyRatedVideos(service)

# for i in range(0,len(videoIds)):
#     videoId=videoIds[i]
#     videoRating=videoRatingItems[i]["rating"]
#     print("{} : {}".format(videoId,videoRating))

# for x in outVideoIds:
#     print(x)

# q = OrderedDict([('e',4),('a',1),('b',2),('a',3)])
# for x in q:
#     print(x)


#subItems = GetSubs(service,"YOURCHANNELID")
#for sub in subItems:
#    print(sub['snippet']["title"])


# aaa=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
# d=2
# print([((i,(i*d,(i*2+d))),aaa[i*d:((i*2+d) if (i*2+d < len(aaa)) else (len(aaa)-1))]) for i in range(0,(len(aaa)+d)//d)])
# print([(i,aaa[i*d:i*d+d]) for i in range(0,(len(aaa)+d-1)//d)])