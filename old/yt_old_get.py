
# def GetPlaylistVideoItems(service,playlistId):
#     playlistItems=[]
#     nextPageToken = None

#     while True:
#         response = service.playlistItems().list(
#             part='contentDetails',
#             playlistId=playlistId,
#             maxResults=50,
#             pageToken=nextPageToken
#         ).execute()

#         playlistItems.extend(response['items'])
#         nextPageToken = response.get('nextPageToken')

#         if nextPageToken==None:
#             break

#         time.sleep(request_delay)

#     return playlistItems

def GetPlaylistVideoIds(service,playlistId):
    videoIds=[]
    nextPageToken = None

    while True:
        time.sleep(request_delay)
        response = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlistId,
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        videoIds.extend([x['contentDetails']['videoId'] for x in response['items']])

        time.sleep(request_delay)
        nextPageToken = response.get('nextPageToken')

        if nextPageToken==None:
            break

    return videoIds
    
def GetVideoTitlesFromIds(service, videoIds):
    ""
    


def GetPlaylistVideoIdsAndTitles(service,playlistId):
    videoIdsAndTitles=[]
    nextPageToken = None

    while True:
        time.sleep(request_delay)
        response = service.playlistItems().list(
            part='snippet',
            playlistId=playlistId,
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        videoIdsAndTitles.extend([(x['snippet']['resourceId']['videoId'],x['snippet']['title']) for x in response['items']])

        time.sleep(request_delay)
        nextPageToken = response.get('nextPageToken')


        if nextPageToken==None:
            break

    return videoIdsAndTitles

# def GetVideoRatingItems(service,videoIds):
#     ratingItems=[]
#     i=0

#     while i<len(videoIds):
#         ids=""

#         for j in range(0,20):
#             ids+=("," if j!=0 else "")+videoIds[i]
#             i+=1

#             if i>= len(videoIds):
#                 break;

#         if ids!="":
#             request = service.videos().getRating(id=ids)
#             response = request.execute()
#             ratingItems.extend(response['items'])
#             # print(response)
#             # print(ids)

#         time.sleep(request_delay)

#     return ratingItems

def GetVideoRatings(service,videoIds):
    ratings=[]
    d=50

    for i in range(0,(len(videoIds)+d-1)//d):
        videoIdsBatch = ','.join(videoIds[i*d:i*d+d])
        request = service.videos().getRating(id=videoIdsBatch)
        response = request.execute()
        ratings.extend(x['rating'] for x in response['items'])
        time.sleep(request_delay)

    return ratings
    

def GetPlaylistUnratedVideoIds(service,srcPlaylistId):
    srcVideoIds=GetPlaylistVideoIds(service, srcPlaylistId)
    srcRating=GetVideoRatings(service, srcVideoIds)

    return [srcVideoIds[i] for i in range(0,len(srcVideoIds))
            if srcRatings[i]=='none']

def GetPlaylistUnratedVideoIdsAndTitles(service,playlistId):
    videoIdsAndTitles=GetPlaylistVideoIdsAndTitles(service,playlistId)
    rating=GetVideoRatings(service, [x[0] for x in videoIdsAndTitles])

    return [videoIdsAndTitles[i] for i in range(0,len(videoIdsAndTitles))
            if rating[i]=='none']

def GetPlaylistRatedVideoIdsAndTitles(service,playlistId):
    videoIdsAndTitles=GetPlaylistVideoIdsAndTitles(service,playlistId)
    rating=GetVideoRatings(service, [x[0] for x in videoIdsAndTitles])

    return [(videoIdsAndTitles[i][0],videoIdsAndTitles[i][1],rating[i])
            for i in range(0,len(videoIdsAndTitles))
            if rating[i]!='none']

def GetPlaylistsUnratedVideoIds(service,playlistIds,exludePlaylistIds):
    allVideoIds = []
    allExcludeVideoIds = []

    #
    for playlistId in playlistIds:
        videoIds=GetPlaylistVideoIds(service, playlistId)
        allVideoIds.extend(videoIds)

    #
    allVideoIdsDict = OrderedDict([(x,0) for x in allVideoIds])

    #
    for exludePlaylistId in exludePlaylistIds:
        videoIds=GetPlaylistVideoIds(service, exludePlaylistId)

        for videoId in videoIds:
            if videoId in allVideoIdsDict:
                del allVideoIdsDict[videoId]

    #
    allVideoIds = [x for x in allVideoIdsDict]
    ratings=GetVideoRatings(service, allVideoIds)
    allVideoIds = [allVideoIds[i] for i,v in enumerate(ratings) if v =='none']

    return allVideoIds


def GetSubs(service,channelId):
    items = []
    Ok=True
    nextPageToken = None

    while Ok:
        request = service.subscriptions().list(
            part="snippet,contentDetails",
            channelId=channelId,
            maxResults=50,
            pageToken=nextPageToken
        )

        response = request.execute()
        items.extend(response['items'])
        nextPageToken = response.get('nextPageToken')
        Ok=nextPageToken!=None

    return items

def GetVideoTitlesAndChannelIds(service,videoIds):
    items=[]
    d=50

    for i in range(0,(len(videoIds)+d-1)//d):
        videoIdsBatch = ','.join(videoIds[i*d:i*d+d])

        time.sleep(request_delay)
        request = service.videos().list(
            part="snippet",
            id=videoIdsBatch,
            maxResults=50
        )

        response = request.execute()
        items.extend(response['items'])

    return [(x['snippet']['title'],x['snippet']['channelId']) for x in items]




def GetMyPlaylistIdsAndTitles(service):
    playlistIdsAndTitles=[]
    nextPageToken = None

    while True:
        time.sleep(request_delay)

        request = service.playlists().list(
            part="contentDetails,snippet",
            maxResults=50,
            mine=True,
            pageToken=nextPageToken
        )

        response = request.execute()
        time.sleep(request_delay)

        nextPageToken = response.get('nextPageToken')
        playlistIdsAndTitles.extend([(x['id'],x['snippet']['title']) for x in response['items']])

        if nextPageToken==None:
            break

    return playlistIdsAndTitles

def GetMyPlaylistTitlesAndIdsDict(service):
    playlistIdsAndTitles=GetMyPlaylistIdsAndTitles(service)
    return dict([(x[1],x[0]) for x in playlistIdsAndTitles])

def GetMyPlaylistId(service,playlistTitle):
    playlistDict=GetMyPlaylistTitlesAndIdsDict(service)
    return playlistDict[playlistTitle] if playlistTitle in playlistDict else None

def GetOrCreateMyPlaylistId(service,playlistTitle):
    playlistId = GetMyPlaylistId(service,playlistTitle)

    if playlistId == None:
        playlistId = CreatePlaylist(service,playlistTitle)

    return playlistId

def GetPlaylistVideoIdsAndItemIds(service,playlistId):
    videoIdsAndItemIds=[]
    nextPageToken = None

    while True:
        time.sleep(request_delay)
        response = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlistId,
            maxResults=50,
            pageToken=nextPageToken
        ).execute()

        videoIdsAndItemIds.extend([(x['contentDetails']['videoId'],x['id']) for x in response['items']])
        time.sleep(request_delay)
        nextPageToken = response.get('nextPageToken')


        if nextPageToken==None:
            break


    return videoIdsAndItemIds
    

def GetDuplicateVideoIds(service,playlistIds):
    videoIdsCount=dict()

    for playlistId in playlistIds:
        videoIds = GetPlaylistVideoIds(service,playlistId)

        for videoId in videoIds:
            if videoId not in videoIdsCount:
                videoIdsCount[videoId]=0

            videoIdsCount[videoId]+=1

    return [k for k,v in videoIdsCount.items() if v>1]

def GetPlaylistsVideoIds(service,playlistIds):
    allVideoIds=[]

    for playlistId in playlistIds:
        videoIds = GetPlaylistVideoIds(service,playlistId)
        allVideoIds.extend(videoIds)

    return list(set(allVideoIds))

def GetPlaylistsRatedVideoIds(service,playlistIds):
    videoIds=GetPlaylistsVideoIds(service,playlistIds)
    ratings=GetVideoRatings(service,videoIds)
    return [v for i,v in enumerate(videoIds) if ratings[i]!='none']



def GetChannelSubIds(service,userChannelId):
    nextPageToken = None
    subs=[]

    while True:
        time.sleep(request_delay)

        request = service.subscriptions().list(
            part="snippet,contentDetails",
            channelId=userChannelId,
            maxResults=50,
            pageToken=nextPageToken
        )

        response = request.execute()
        nextPageToken = response.get('nextPageToken')

        for x in response['items']:
            cid=x['snippet']['resourceId']['channelId']
            subs.append(cid)

        if nextPageToken==None:
            break

    return subs
    

def get_sub_ids(service,userChannelId,channelIds):
    # nextPageToken = None

    subIds=[]
    d=50

    for i in range(0,(len(channelIds)+d-1)//d):
        channelIdStr = ','.join(channelIds[i*d:i*d+d])

        request = service.subscriptions().list(
            part="id",
            channelId=userChannelId,
            forChannelId=channelIdStr,
            maxResults=50
            # pageToken=nextPageToken
        )

        response = request.execute()
        subIds.extend([x['id'] for x in response['items']])

        # print(response)
        # nextPageToken = response.get('nextPageToken')

        # for i in response['items']:
        #     print(i['snippet']['title'])

        # if nextPageToken==None:
        #     break

    return subIds
    

def GetVideoCountOld(service,channelId):
    count=0
    nextPageToken = None
    d = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')
    # d = datetime.datetime.now(datetime.timezone.utc).isoformat()

    while True:
        time.sleep(request_delay)
        request = service.search().list(
            part="snippet",
            channelId=channelId,
            maxResults=50,
            order="date",
            publishedAfter=d, #"2021-10-02T00:00:00Z",
            pageToken=nextPageToken
        )

        response = request.execute()
        nextPageToken = response.get('nextPageToken')

        # for i in response['items']:
        #     print(i['snippet']['title'])

        count+=len(response['items'])

        if nextPageToken==None:
            break

    return count

def GetVideoCount(service,channelId,inDays=0):
    playlistId = re.sub('UC(.*)','UU\\1',channelId)
    d = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=inDays)
    d=d.strftime('%Y-%m-%dT%H:%M:%SZ')
    # d = datetime.datetime.now(datetime.timezone.utc).isoformat()

    count = 0
    nextPageToken = None

    while True:
        time.sleep(request_delay)

        try:
            response = service.playlistItems().list(
                part='contentDetails',
                playlistId=playlistId,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()

            for x in response['items']:
                videoPublishedAt=x['contentDetails']['videoPublishedAt']

                if inDays != 0 and videoPublishedAt < d:
                    return count

                count+=1

            nextPageToken = response.get('nextPageToken')

            if nextPageToken==None:
                break

        except googleapiclient.errors.HttpError as e:
            return -1 if count == 0 else count

    return count

def GetChannelDead(service,channelId, inMaxUploadCount=0, inDays = 300):

    playlistId = re.sub('UC(.*)','UU\\1',channelId)
    d = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=inDays)
    d=d.strftime('%Y-%m-%dT%H:%M:%SZ')

    count = 0
    nextPageToken = None

    while True:
        time.sleep(request_delay)

        try:
            response = service.playlistItems().list(
                part='contentDetails',
                playlistId=playlistId,
                maxResults=50,
                pageToken=nextPageToken
            ).execute()

            for x in response['items']:
                videoPublishedAt=x['contentDetails']['videoPublishedAt']

                if videoPublishedAt < d:
                    break

                count+=1

            if count > inMaxUploadCount:
                return False

            nextPageToken = response.get('nextPageToken')

            if nextPageToken==None:
                break

        except googleapiclient.errors.HttpError as e:
            return True

    return True

def GetHasVideos(service,channelId):
    playlistId = re.sub('UC(.*)','UU\\1',channelId)
    time.sleep(request_delay)

    try:
        response = service.playlistItems().list(
            part='contentDetails',
            playlistId=playlistId,
            maxResults=1
        ).execute()

        return len(response['items']) != 0
    except googleapiclient.errors.HttpError as e:
        ''
        # print(e)

    return False

############################
            

def GetPlaylistVideoIds(service,playlistId):
    items=GetList(service.playlistItems(), {'part':'contentDetails','playlistId':playlistId})
    return [x['contentDetails']['videoId'] for x in items]

def GetVideosInfo(service,videoIds):
    items = GetListBatch(service.videos(), {'part':'snippet'}, 'id', videoIds)
    return [{
        'videoId' : x['id'],
        'videoTitle' : x['snippet']['title'],
        'channelId' : x['snippet']['channelId'],
        'channelTitle' : x['snippet']['channelTitle'],
        'publishedAt' : x['snippet']['publishedAt']
    } for x in items]

videoIds=yt.GetPlaylistsVideoIds(service,playlistIds)
videoInfos = GetVideosInfo(service,videoIds)

################


##########################
