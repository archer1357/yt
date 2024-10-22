import glob, os, bs4, re
import csv, json, string

import pathlib


import sys
sys.path.append("..")
import yt,utils

pathlib.Path("input").mkdir(parents=True, exist_ok=True)
pathlib.Path("output").mkdir(parents=True, exist_ok=True)



service = yt.Create_Service2('b','..')
print(service)

inputFileNames = utils.GetBookmarkFilesInDir('input')
outputFileNames = [fn.replace("input","output") for fn in inputFileNames]
inputFilesLines = [utils.ReadFileLines(fn) for fn in inputFileNames]

print("'{}' '{}'".format(inputFileNames,outputFileNames))

for i in range(0,len(inputFileNames)):

    with open(outputFileNames[i], "w", encoding='utf-8') as file:
        for line in inputFilesLines[i]:
            channelId = utils.GetBookmarkLineChannelId(line)

            if channelId == None:
                file.write(line)
                continue

            print(channelId)
            if yt.GetChannelDead(service,channelId,1,30*3):
                file.write(line)
                print("d")
