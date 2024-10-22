import glob, os, bs4, re

import csv, json, string
import sys
sys.path.append("..")

import yt

def ReadFileLines(fn):
    with open(fn) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        return lines




service = yt.Create_Service2('b3','..')
print(service)
channelIds=ReadFileLines('channels2.txt')
yt.SubscribeChannels(service, channelIds)


# service = yt.Create_Service2('b2','..')
# print(service)
# yt.UnsubscribeChannels(service, channelIds)

# channelIds=ReadFileLines('channels.txt')
# channelIds=['CHANNELID']
# userChannelId=yt.GetMyChannelId(service)
# subIds=yt.get_sub_ids(service,userChannelId,channelIds)
# print(len(subIds))
# for x in subIds:
#     print(x)
