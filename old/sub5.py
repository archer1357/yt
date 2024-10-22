import glob, os, bs4, re

import csv, json, string




import sys
sys.path.append("..")
import yt


def readCsvFile(fn):
    with open(fn, newline='', encoding="utf8") as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='"')
        return [(row[2],row[0]) for i,row in enumerate(rows)
                if i!=0 and len(row)!=0]



def writeLinks(fn,rows,hasSet=set()):
    with open(fn, "w", encoding='utf-8') as file:
        for row in rows:
            name=row[0]
            id=row[1]

            if id in hasSet:
                continue

            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">"{}"</a>\n'.format(id,name)
            file.write(s)




def fixName(n):
    return re.sub('^\([0-9]+\) ', '', n)

def fixFileName(n):
    return re.sub('^(.*)bookmarks_([0-9]+)_([0-9]+)_([0-9]+)([a-z]*).html$',
                  '\\1bookmarks_\\4_\\3_\\2\\5.html', n)

def readHtmlFile(fn):
    with open(fn,'rb') as f:
        return bs4.BeautifulSoup(f, 'html5lib')

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

def readHtmlFileChannelNamesAndIds(fn):
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
        outs.append((name,id))

    return outs

# hasSet=set(readHtmlFileChannelIds('bookmarks_24_10_2021.html'))

# bm=readHtmlFileChannelNamesAndIds('out2.html')


# writeLinks('out5.html',bm,hasSet)




service = yt.Create_Service2('a','..')
print(service)


bm=readHtmlFileChannelNamesAndIds('out5.html')

doesHave=[]
doesntHave=[]

for row in bm:
    name=row[0]
    id=row[1]

    h=yt.GetHasVideos(service,id)

    if h:
        doesHave.append(row)
    else:
        doesntHave.append(row)

    print("{} = {}".format(id,h))

writeLinks('out6a.html',doesHave)
writeLinks('out6b.html',doesntHave)
