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


bm=readHtmlFile('z.html')
elements = bm.find_all("a")

with open('out.txt', "w") as file:
    for e in elements:
        name = fixName(e.text)
        link = e["href"]

        if not re.match('.*www[.]youtube.*',link):
            # print(link)
            continue

        name = re.sub(' - YouTube','',name)
        id=re.sub('^.*//.*/(.*)/.*', '\\1', link)


        file.write(id + "\n")
