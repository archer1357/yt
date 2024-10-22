import glob, os, bs4, re

import csv, json, string




import sys
sys.path.append("..")
import yt



def writeLinks(fn,rows,hasSet=set()):
    c = 0

    with open(fn, "w", encoding='utf-8') as file:
        for row in rows:
            c+=1
            id=row[0]
            name=row[1]

            if id in hasSet:
                continue

            s='<br/>{} <a href="https://www.youtube.com/channel/{}/videos" target="_blank">{}</a>\n'.format(c,id,name)
            file.write(s)



def GetChannelSubsInfo(service,userChannelId):
    items=yt.GetList(service.subscriptions(), {
        'part':'snippet,contentDetails',
        # order="SUBSCRIPTION_ORDER_RELEVANCE",
        # order="alphabetical",
        # order="relevance",
        # order="unread",
        # mySubscribers=True,
        # mine=True,
        'channelId':userChannelId
    })

    return [(
        x['snippet']['resourceId']['channelId'],
        x['snippet']['title'],
        x['snippet']['publishedAt']
    ) for x in items]

dups = dict()

hasSet=set()

allSubs=[]

service = yt.Create_Service2('b','..')
print(service)

myChannels=[

    ('CHANNELID1','1'),
    ('CHANNELID2','2')
    ]

i = 0

while os.path.exists("out{:03d}".format(i)):
    i += 1

outdir="out{:03d}".format(i)
print("outdir = {}".format(outdir))
os.mkdir(outdir)



total=0

for userChannelId,myChannelName in myChannels:
    myChannelName2=myChannelName.replace(" ", "_")

    print("{} {}".format(userChannelId,myChannelName2))


    subInfos=GetChannelSubsInfo(service,userChannelId)
    #if myChannelName != 'somename':
    #    hasSet.update(set([x[0] for x in subInfos]))
    ## subInfos= [(x[2],x[0]) for x in subInfos]

    for x in subInfos:
        channelId=x[0]

        #if myChannelName!='somename':
        #    allSubs.append(x[0:2])

        if channelId not in dups:
            dups[channelId]=(x[1],[])

        dups[channelId][1].append(myChannelName)

    n=len(subInfos)
    writeLinks('{}/{} ({}).html'.format(outdir,myChannelName2,n),subInfos)

    total+=n

    print("     = {}".format(n))


writeLinks('{}/out.html'.format(outdir),subInfos,hasSet)

for k,v in dups.items():
    myChannelNames=v[1]

    for i in range(0,len(myChannelNames)):
        #if myChannelNames[i]=='somename':
        #    del myChannelNames[i]

with open('{}/dups.html'.format(outdir), "w", encoding='utf-8') as file:
    for k,v in dups.items():
        videoName=v[0]
        myChannelNames=v[1]

        if len(myChannelNames) > 1:
            id=k
            name=videoName
            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">{}</a>\n'.format(id,name)
            file.write(s)

            file.write('<ul>')

            for x in myChannelNames:
                file.write('<li>{}</li>'.format(x))

            file.write('</ul>')

# def f7(seq):
#     seen = set()
#     seen_add = seen.add
#     return [x for x in seq if not (x in seen or seen_add(x))]
# for x in allSubs:
#     print(x)
allSubs2=dict(allSubs).items()

writeLinks('{}/all.html'.format(outdir),allSubs2)

with open('{}/all2.txt'.format(outdir), "w", encoding='utf-8') as file:
    for k,v in dups.items():
        file.write("{}\n".format(k))
with open('{}/all3.txt'.format(outdir), "w", encoding='utf-8') as file:
    for k,v in allSubs2:
        file.write("{}\n".format(k))
# GetMyChannelId(service)
# a=[(1,2,3),(4,5,6)]
# print([(x,y) for x,y,z in a])



#
# writeLinks('out6b.html',doesntHave)
