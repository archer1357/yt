
def CreatePlaylist(service,name):
    request = service.playlists().insert(
        part="snippet,status",
        body={
          "snippet": {
            "title": name
          },
          "status": {
            "privacyStatus": "unlisted"
          }
        }
    )
    response = request.execute()
    return response['id']

def AddVideosToPlaylist(service,videoIds,playlistId):
    for videoId in videoIds:
        try:
            time.sleep(request_delay)
            service.playlistItems().insert(
                part='snippet',
                body= {
                    'snippet': {
                        'playlistId': playlistId,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': videoId
                        }
                    }
                }
            ).execute()

            print("video added: {}".format(videoId))

        except Exception as e:
            print("video add failed: {}".format(videoId))
            print(e)
            


def add_subscription(service, channel_id):
    time.sleep(request_delay)

    add_subscription_response = service.subscriptions().insert(
        part='snippet',
        body={
            'snippet': {
                'resourceId': {
                    'channelId':channel_id
                }
            }
        }).execute()

    return add_subscription_response['snippet']['title']

###########################

def AddNonDuplVideosToPlaylist(service,videoIds,playlistId):
    existingVideoIds=set(GetPlaylistVideoIds(service,playlistId))
    nonDuplVideoIds = [x for x in videoIds if x not in existingVideoIds]
    AddVideosToPlaylist(service,nonDuplVideoIds,playlistId)
    

def SubscribeChannels(service, channelIds):
    for channelId in channelIds:
        add_subscription(service, channelId)
        print(channelId)

def SubscribeChannelsSafe(service, channelIds):
    userChannelId=GetMyChannelId(service)
    subbedChannelIds=GetChannelSubIds(service,userChannelId)
    channelIds=list(set(channelIds)-set(subbedChannelIds))
    SubscribeChannels(service, channelIds)
