import glob, os, bs4, re
import csv, json, string

import pathlib


import sys
sys.path.append("..")
import yt,utils

pathlib.Path("input").mkdir(parents=True, exist_ok=True)
pathlib.Path("output").mkdir(parents=True, exist_ok=True)
inputFileNames = utils.GetBookmarkFilesInDir('input')
outputFileNames = [fn.replace("input","output") for fn in inputFileNames]


print("'{}' '{}'".format(inputFileNames,outputFileNames))

for i in range(0,len(inputFileNames)):
    lines=utils.ReadFileLines(inputFileNames[i])
    channelIds=[]

    for line in lines:
        channelId = utils.GetBookmarkLineChannelId(line)

        if channelId != None:
            channelIds.append(channelId)

    if len(channelIds)>0:
        with open(outputFileNames[i]+'.txt', "w", encoding='utf-8') as file:
            file.write('[')

            for j,channelId in enumerate(channelIds):
                file.write("{}'{}'".format(', ' if j!=0 else '',channelId))

            file.write(']')
