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


service = yt.Create_Service2('a','..')
print(service)

# print(yt.GetVideoCount2(service,''))

hasIds=set(readHtmlFileChannelIds('bookmarks_13_10_2021.html'))

subs_csv=readCsvFile('subscriptions.csv')

channels=[]
channels2=[]
missing=[]
c=0

for row in subs_csv:
    name=row[0]
    id=row[1]

    togo=len(subs_csv)-c-1

    try:

        num = yt.GetVideoCount2(service,id,365)

        if id not in hasIds:
            channels.append([id,name,num])
        else:
            channels2.append([id,name,num])

        print('{} - {} : {}'.format(togo,num,id))

    except Exception as e:
        missing.append([id,name])
        print('{} - err : {}'.format(togo,id))

    c+=1

channels.sort(key=lambda x: x[2], reverse=True)
channels2.sort(key=lambda x: x[2], reverse=True)

if len(channels) > 0:
    with open('out.html', "w", encoding='utf-8') as file:
        c = 0

        for row in channels:
            id=row[0]
            name=row[1]
            num=row[2]
            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">{} - "{}"</a>\n'.format(id,num,name)
            file.write(s)
            c+=1

if len(channels2) > 0:
    with open('out2.html', "w", encoding='utf-8') as file:
        c = 0

        for row in channels2:
            id=row[0]
            name=row[1]
            num=row[2]
            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">{} - "{}"</a>\n'.format(id,num,name)
            file.write(s)
            c+=1

if len(missing) > 0:
    with open('missing.html', "w", encoding='utf-8') as file:
        c = 0

        for row in missing:
            id=row[0]
            name=row[1]

            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">{} - "{}"</a>\n'.format(id,c,name)
            file.write(s)
            c+=1
