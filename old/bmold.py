# for x in sorted(getFilesInDir("a"),key=lambda n : fixFileName(n), reverse=True):
#     print(fixFileName(x))

# print(fixFileName("bookmarks_22_09_2021b.html"))

# print(getFilesInDir("a"))
# print(getFilesInDir("b"))


def extractFileData(fn):
    outputs=[]

    soup=readHtmlFile(fn)
    elements = soup.find_all("a")

    for e in elements:
        path=[]
        dl=e.find_parent('dl')

        while dl:
            h=dl.find_previous_sibling('h3')

            if not h:
                break

            path.insert(0,h.text)
            dl=dl.find_parent('dl')

        if path[0]=='Bookmarks bar':
            del path[0]

        # if len(path)>0 and path[0]=='c':
        #     path[0]='z'

        if len(path)>0 and path[0]=='unsorted':
            path[0]='0unsorted'
        outputs.append([fixName(e.text),e["href"],path])

    return outputs



for fn in getFilesInDir("b"):
    ds=extractFileData(fn)

    for d in ds:
        ignores.add(d[0])
        ignores.add(d[1])


# for a in ignores:
#     print(a)

# keeps={}
allLinks=[]

# unsorted=[]

for fn in sorted(getFilesInDir("a"),key=fixFileName, reverse=True):
    ds=extractFileData(fn)
    allLinks.extend(ds)

    # for d in ds:
    #     path=d[2]

    #     if len(path>0 and path[-1])
    #     allLinks.append(d)

allLinks.sort(key=lambda x: '/'.join(x[2]), reverse=True)


links=[]

for d in allLinks:
    name=d[0]
    url=d[1]
    path=d[2]
    # print(d)
    # if len(path)>0 and path[-1]=='unsorted':
    #     unsorted.append(d)

    if name in ignores or url in ignores:
        continue

    ignores.add(name)
    ignores.add(url)

    links.append(d)

# for d in unsorted:
#     name=d[0]
#     url=d[1]
#     path=d[2]

#     if name in ignores or url in ignores:
#         continue

#     ignores.add(name)
#     ignores.add(url)

#     links.append(d)

orderedLinks={}

for link in links:
    path=link[2]
    pathName='/'.join(path)
    if pathName not in orderedLinks:
        orderedLinks[pathName] = []

    orderedLinks[pathName].append(link)

# dones=set()

# links=[]
# for k,v in keeps:
#     if k in dones:
#         continue

#     dones.add(v[0])
#     dones.add(v[1])

#     links.append()
# orderedLinks.sort()
# sortOrders = sorted(orderedLinks.items(), key=lambda x: x[0], reverse=True)

with open('out.html', 'wb') as f:
    f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3 ADD_DATE="1624352054" LAST_MODIFIED="1632885751" PERSONAL_TOOLBAR_FOLDER="true">Bookmarks bar</H3>
    <DL><p>
""".encode('utf8'))

    for k,v in orderedLinks.items():
        f.write("""        <DT><H3 ADD_DATE="1627717826" LAST_MODIFIED="1631982480">{}</H3>
        <DL><p>
""".format(k).encode('utf8'))


        # f.write('<p><h3>{}</h3></p>'.format(k).encode('utf8'))

        for x in v:
            # f.write('<a href="{}">{}</a><br />'.format(x[1],x[0]).encode('utf8'))
            f.write('            <DT><A href="{}">{}</A>\n'.format(x[1],x[0]).encode('utf8'))

        f.write('        </DL><p>\n'.encode('utf8'))
    f.write('    </p></DL>\n'.encode('utf8'))
    f.write('</p></DL>\n'.encode('utf8'))

    f.write("""        </DL><p>
    </DL><p>
</DL><p>
""".encode('utf8'))
