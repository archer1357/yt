import glob, os, bs4, re

import csv, json, string




import sys




def fixName(n):
    return re.sub('^\([0-9]+\) ', '', n)

def fixFileName(n):
    return re.sub('^(.*)bookmarks_([0-9]+)_([0-9]+)_([0-9]+)([a-z]*).html$',
                  '\\1bookmarks_\\4_\\3_\\2\\5.html', n)

def readHtmlFile(fn):
    with open(fn,'rb') as f:
        return bs4.BeautifulSoup(f, 'html5lib')


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

def writeLinks(fn,rows,hasSet=set()):
    with open(fn, "w", encoding='utf-8') as file:
        for row in rows:
            name=row[0]
            id=row[1]

            if id in hasSet:
                continue

            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">"{}"</a>\n'.format(id,name)
            file.write(s)

a=dict([(x[1],x[0]) for x in readHtmlFileChannelNamesAndIds('a.html')])
b=dict([(x[1],x[0]) for x in readHtmlFileChannelNamesAndIds('b.html')])

links=[(v,k) for k,v in a.items() if k not in b]


writeLinks("outttt.html",links)

for i in range(0,2):
    print(i*2-1)
