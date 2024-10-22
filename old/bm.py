import glob, os, bs4, re

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

ignores=set()
files = getFilesInDir('a')

if not os.path.exists('b'):
    os.makedirs('b')

root_soup = bs4.BeautifulSoup("<html>a web page</html>", 'html.parser')
c=0
for fileName in files:
    # print(fileName)
    outFileName = re.sub('^a','b',fileName)
    outFileName = fixFileName(outFileName)
    print(outFileName)

    soup=readHtmlFile(fileName)
    elements = soup.find_all("a")

    for e in elements:
        name = e.text
        fname = fixName(name)
        link = e["href"]

        if name in ignores or link in ignores or fname in ignores:
            e.find_parent('dt').decompose()
            # e.decompose()

        ignores.add(name)
        ignores.add(fname)
        ignores.add(link)

    hs=soup.find_all("h3")

    for h in hs:
        if h.parent and len(h.parent.find_all("a")) == 0:
            h.parent.decompose()

    if(len(soup.find_all("a")) > 0):
        with open(outFileName, "w", encoding='utf-8') as file:
            file.write(str(soup))

        if c!=0 :
            root_soup.append(soup)

    c+=1

with open('out.html', "w", encoding='utf-8') as file:
    file.write(str(root_soup))
