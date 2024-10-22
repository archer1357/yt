import glob, os, bs4, re

import csv, json, string
import sys


def readCsvFile(fn):
    with open(fn, newline='', encoding="utf8") as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='"')
        return [(row[2],row[0]) for i,row in enumerate(rows)
                if i!=0 and len(row)!=0]



def writeLinks(fn,rows,hasSet):
    with open(fn, "w", encoding='utf-8') as file:
        for row in rows:
            name=row[0]
            id=row[1]

            if id in hasSet:
                continue

            s='<br/><a href="https://www.youtube.com/channel/{}/videos" target="_blank">"{}"</a>\n'.format(id,name)
            file.write(s)





# subs_csv0=readCsvFile('subscriptions0.csv')
# subs_csv1=readCsvFile('subscriptions1.csv')
subs_csv2=readCsvFile('subscriptions2.csv')

# hasSet=set([x[1] for x in (subs_csv1+subs_csv2)])
# writeLinks('out2.html',subs_csv0,hasSet)

hasSet=set([x[1] for x in subs_csv2])
subs_csv2b=readCsvFile('subscriptions2b.csv')

writeLinks('out3.html',subs_csv2b,hasSet)
