import glob, os, bs4, re

import csv, json, string
import sys
sys.path.append("..")

import yt

def fixName(n):
    return re.sub('^\([0-9]+\) ', '', n)

def fixFileName(n):
    return re.sub('^(.*)bookmarks_([0-9]+)_([0-9]+)_([0-9]+)([a-z]*).html$',
                  '\\1bookmarks_\\4_\\3_\\2\\5.html', n)

def readHtmlFile(fn):
    with open(fn,'rb') as f:
        return bs4.BeautifulSoup(f, 'html5lib')

def getFilesInDir(dir):
    files = [x for x in glob.glob("{}/*.html".format(dir))]
    files.sort(key=fixFileName, reverse=True)
    return files

def readCsvFile(fn):
    with open(fn, newline='', encoding="utf8") as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='"')
        return [(row[2],row[0]) for i,row in enumerate(rows)
                if i!=0 and len(row)!=0]




def readHtmlFileChannelIds(fn):
    soup=readHtmlFile(fn)
    elements = soup.find_all("a")
    ids=[]

    for e in elements:
        name = fixName(e.text)
        link = e["href"]

        if not re.match('.*www[.]youtube.*',link):
            continue

        name = re.sub(' - YouTube','',name)
        id=re.sub('^.*//.*/(.*)/.*', '\\1', link)
        ids.append(id)

    return ids


def readHtmlFileChannelNamesIds(fn):
    soup=readHtmlFile(fn)
    elements = soup.find_all("a")
    outs=[]

    for e in elements:
        name = fixName(e.text)
        link = e["href"]

        if not re.match('.*www[.]youtube.*',link):
            continue

        name = re.sub(' - YouTube','',name)
        id=re.sub('^.*//.*/(.*)/.*', '\\1', link)
        outs.append([name,id])

    return outs

service = yt.Create_Service2('b','..')
print(service)


# subs_csv=readCsvFile('subscriptions.csv')

channels=[]
c=0

subInfos=yt.GetChannelSubsInfo(service,'CHANNELID')

subs = [[x[1],x[0]] for x in subInfos]
# for x in subInfos:
#     print(x)
# subs= readHtmlFileChannelNamesIds('bookmark.html')



# print(len(subs_csv))
for row in subs:
    name=row[0]
    id=row[1]
    # print('{} : {}'.format(name,id))

    togo=len(subs)-c-1

    try:

        num = yt.GetVideoCount(service,id,31)


        channels.append([id,name,num])



        print('{} - {} : {}'.format(togo,num,id))

    except Exception as e:
        print(e)
        channels.append([id,name,0])
        print('{} - err : {}'.format(togo,id))

    c+=1

channels.sort(key=lambda x: x[2], reverse=True)

if len(channels) > 0:
    with open('out2.html', "w", encoding='utf-8') as file:
        c = 0

        for row in channels:
            id=row[0]
            name=row[1]
            num=row[2]
            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">{} - "{}"</a>\n'.format(id,num,name)
            file.write(s)
            c+=1
