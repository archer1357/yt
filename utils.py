import glob, os, bs4, re
import csv, json, string

def FixBookmarkFileName(n):
    return re.sub('^(.*)bookmarks_([0-9]+)_([0-9]+)_([0-9]+)([a-z]*).html$',
                  '\\1bookmarks_\\4_\\3_\\2\\5.html', n)

def GetBookmarkFilesInDir(dir):
    files = [x for x in glob.glob("{}/*.html".format(dir))]
    files.sort(key=FixBookmarkFileName, reverse=True)
    return files

def ReadFileLines(fn,strip=False):
    with open(fn, "r", encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines] if strip else lines
        return lines

def GetBookmarkLineChannelId(line):
    result=re.subn('^.*https://www.youtube.com/channel/([-_a-zA-Z0-9]+)/videos.*\r?\n$','\\1',line)
    return None if result[1] == 0 else result[0]

def GetBookmarkLineChannelName(line):
    ""

def ReadHtmlLines(fn,strip=False):
    with open(fn, "r", encoding='utf-8') as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines] if strip else lines
        return lines

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
