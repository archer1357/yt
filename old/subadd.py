import glob, os, bs4, re

import csv, json, string
import sys
sys.path.append("..")

import yt
import utils







service = yt.Create_Service2('channelname','..')
print(service)

userChannelId=yt.GetMyChannelId(service)
print('my {}'.format(userChannelId))

channelIds=utils.readHtmlFileChannelIds('bookmarkfile.html')
subInfos=yt.GetChannelSubsInfo(service,userChannelId)
hasChannelIds = set([x[0] for x in subInfos])


for channelId in channelIds:
    if channelId not in hasChannelIds:
        print(channelId)
        yt.add_subscription(service, channelId)
