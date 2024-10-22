
def RemoveVideoIdsFromMyPlaylist(service,videoIds,playlistId):
    videoItemDict = dict(GetPlaylistVideoIdsAndItemIds(service,playlistId))
    videoItemIdsToRemove = [(videoItemDict[x],x) for x in videoIds if x in videoItemDict]

    # print("videoItemDict={} videoItemIdsToRemove={}".format(len(videoItemDict),len(videoItemIdsToRemove)))
    # print(videoIds)
    # print(videoItemDict)
    # print(videoItemIdsToRemove)
    for (videoItemId,videoId) in videoItemIdsToRemove:
        time.sleep(request_delay)
        print("removing {} {}".format(videoItemId,videoId))
        request = service.playlistItems().delete(
            id=videoItemId
        )
        request.execute()



def remove_subscription(service, sub_id):
    time.sleep(request_delay)
    request = service.subscriptions().delete(
        id=sub_id
    )

    response=request.execute()


    return response

###################

def RemovePlaylistsVideosFromMyPlaylist(service,removePlaylistIds,myPlaylistId):
    removeVideoIds=[]

    for removePlaylistId in removePlaylistIds:
        videoIds=GetPlaylistVideoIds(service,removePlaylistId)
        removeVideoIds.extend(videoIds)
    # print("RemovePlaylistsVideosFromMyPlaylist removeVideoIds = {}".format(len(removeVideoIds)))
    RemoveVideoIdsFromMyPlaylist(service,removeVideoIds,myPlaylistId)


def UnsubscribeChannels(service, channelIds):
    d=50
    userChannelId=GetMyChannelId(service)

    for i in range(0,(len(channelIds)+d-1)//d):
        channelIds2=channelIds[i*d:i*d+d]
        subIds=get_sub_ids(service,userChannelId,channelIds2)

        for j,subId in enumerate(subIds):
            remove_subscription(service, subId)
            print(channelIds2[j])