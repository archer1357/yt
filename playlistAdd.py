import glob, os, bs4, re

import csv, json, string
import sys
# sys.path.append("..")

import yt

import time

from collections import OrderedDict

request_delay = 1.0

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


def GetPlaylistVideoIds(service,playlistId):
    items=yt.GetList(service.playlistItems(), {'part':'contentDetails','playlistId':playlistId})
    return [x['contentDetails']['videoId'] for x in items]


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


def AddNonDuplVideosToPlaylist(service,videoIds,playlistId):
    existingVideoIds=set(GetPlaylistVideoIds(service,playlistId))
    nonDuplVideoIds = [x for x in videoIds if x not in existingVideoIds]
    AddVideosToPlaylist(service,nonDuplVideoIds,playlistId)

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

# service = yt.Create_Service2('b')
# print(service)




# myPlaylistId=yt.GetOrCreateMyPlaylistId(service,"w0")
# playlistIds=[]
# # playlistIds.append(yt.GetMyPlaylistId(service,'Watch later'))
# exludePlaylistIds=[myPlaylistId]
# outVideoIds=yt.GetPlaylistsUnratedVideoIds(service,playlistIds,exludePlaylistIds)

# for x in outVideoIds:
#     print(x)

# yt.AddNonDuplVideosToPlaylist(service,outVideoIds,myPlaylistId)


def GetPlaylistsVideoIds(service,playlistIds):
    allVideoIds=[]

    for playlistId in playlistIds:
        videoIds = GetPlaylistVideoIds(service,playlistId)
        allVideoIds.extend(videoIds)


service = yt.Create_Service2('a')



def AddToPlaylist(myPlaylistName,inPlaylists,inExcludePlaylists=[],ignoreRated=True):
    print(myPlaylistName)
    myPlaylistId=GetOrCreateMyPlaylistId(service,myPlaylistName)
    playlistIds=inPlaylists
    exludePlaylistIds=[myPlaylistId]
    exludePlaylistIds.extend(inExcludePlaylists)

    if ignoreRated:
        outVideoIds=GetPlaylistsUnratedVideoIds(service,playlistIds,exludePlaylistIds)
    else:
        outVideoIds=GetPlaylistsVideoIds(service,playlistIds)

    AddNonDuplVideosToPlaylist(service,outVideoIds,myPlaylistId)



##############################


# myPlaylistId=GetOrCreateMyPlaylistId(service,"")
# playlistIds=['']
# exludePlaylistIds=[myPlaylistId]
# outVideoIds=GetPlaylistsUnratedVideoIds(service,playlistIds,exludePlaylistIds)
# AddNonDuplVideosToPlaylist(service,outVideoIds,myPlaylistId)

# myPlaylistId=GetOrCreateMyPlaylistId(service,"channelname")
# playlistIds=['PLAYLISTID']
# exludePlaylistIds=[myPlaylistId]
# outVideoIds=GetPlaylistsUnratedVideoIds(service,playlistIds,exludePlaylistIds)
# AddVideosToPlaylist(service,outVideoIds,myPlaylistId)
##########################

# myPlaylistId=GetOrCreateMyPlaylistId(service,"music")
# print("myPlaylistId {}".format(myPlaylistId))
# playlistIds=['PLAYLISTID']
# exludePlaylistIds=[myPlaylistId]
# outVideoIds=GetPlaylistsUnratedVideoIds(service,playlistIds,exludePlaylistIds)
# print("video ids num is {}".format(len(outVideoIds)))
# # AddVideosToPlaylist(service,outVideoIds,myPlaylistId)
# # AddNonDuplVideosToPlaylist(service,outVideoIds,myPlaylistId)

#############

# AddToPlaylist('playlistname',['PLAYLISTID1','PLAYLISTID2'])
# AddToPlaylist('playlistname',['PLAYLISTID'])



# AddToPlaylist('josephanderson',['PLAYLISTID'])
# # AddToPlaylist('',[''])
# AddToPlaylist('playlistname',['PLAYLISTID'],[],False)
