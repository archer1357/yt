import glob, os, bs4, re

import csv, json, string

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


with open('bookmarks_06_10_2021ee.html', "r", encoding='utf-8') as file:
    bmFile = file.read()

# print(bmFile)

subscsv=readCsvFile('subscriptions.csv')
subNameById={}
subIdByName={}

for row in subscsv:
    name=row[0]
    id=row[1]
    subNameById[id]=name
    subIdByName[name]=id
    # print(row)

bm=readHtmlFile('bookmarks_06_10_2021ee.html')
elements = bm.find_all("a")

for e in elements:
    name = fixName(e.text)
    link = e["href"]

    if not re.match('.*www[.]youtube.*',link):
        # print(link)
        continue

    name = re.sub(' - YouTube','',name)
    id=re.sub('^.*//.*/(.*)/.*', '\\1', link)

    if id in subNameById:
        continue
    if not name in subIdByName:
        print([name,id])
        continue

    id=subIdByName[name]
    # print(name)
    print(id)

    bmFile=bmFile.replace(link,'https://www.youtube.com/channel/{}/videos'.format(id))


with open('outbookmark.html', "w", encoding='utf-8') as file:
    file.write(bmFile)

soup=readHtmlFile('g.html')
elements = soup.find_all("a")
rss=[]
for e in elements:
    link = e["href"]

    if not re.match('.*www[.]youtube.*',link):
        continue
    id=re.sub('^.*//.*/(.*)/.*', '\\1', link)
    rss.append(id)

with open('g.rss', "w") as file:
    for x in rss:
        file.write('https://www.youtube.com/feeds/videos.xml?channel_id={}\n'.format(x))
