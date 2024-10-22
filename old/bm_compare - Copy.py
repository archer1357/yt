import os,re,glob

def fixFileName(n):
    return re.sub('^(.*)bookmarks_([0-9]+)_([0-9]+)_([0-9]+)([a-z]*).html$',
                  '\\1bookmarks_\\4_\\3_\\2\\5.html', n)


def getFilesInDir(dir):
    files = [x for x in glob.glob("{}/*.html".format(dir))]
    files.sort(key=fixFileName, reverse=True)
    return files

def ReadFileLines(fn):
    with open(fn, "r", encoding='utf-8') as file:
        lines = file.readlines()
        # lines = [line.rstrip() for line in lines]
        return lines

def GetLinkChannelID(line):
    channelId_result=re.subn('^.*https://www.youtube.com/channel/([-_a-zA-Z0-9]+)/videos.*\r?\n$','\\1',line)

    return None if channelId_result[1] == 0 else channelId_result[0]

def IsNotChannelLink(line):
    return None == re.match('^.*<A.*$',line)

input_file_names = getFilesInDir('input')

# for i in input_file_names:
#     print(i)

input_files_lines=[]

for file_name in input_file_names:

    lines=ReadFileLines(file_name)
    input_files_lines.append(lines)

    # print('{} - {}'.format(file_name,len(lines)))

dups = dict()

for lines in input_files_lines:
    for line in lines:

        channelId = GetLinkChannelID(line)

        if channelId == None:
            continue

        if channelId not in dups:
            dups[channelId]=0

        dups[channelId]+=1

        # print("'{}'".format(channelId))

input_files_lines2=[]
input_file_names2=[]

for i in range(0,len(input_file_names)):
    input_file_name=input_file_names[i]
    input_file_lines= input_files_lines[i]

    channel_link_count = 0

    input_file_lines2 = []

    for line in input_file_lines:

        channelId = GetLinkChannelID(line)

        if channelId == None:
            if IsNotChannelLink(line):
                input_file_lines2.append(line)

            continue



        if dups[channelId]==1:
            input_file_lines2.append(line)
            channel_link_count+=1


    if channel_link_count > 0:
        input_files_lines2.append(input_file_lines2)
        input_file_names2.append(input_file_name)

# print(input_files_lines2)
print(input_file_names2)
for i in range(0,len(input_file_names2)):
    input_file_name=input_file_names2[i]
    input_file_lines= input_files_lines2[i]


    output_file_name=re.sub('input(.*)','output\\1',input_file_name)
    output_file_name=fixFileName(output_file_name)

    print(input_file_name)
    print(output_file_name)

    if len(input_file_lines) == 0:
        continue

    with open(output_file_name, "w", encoding='utf-8') as file:
        for line in input_file_lines:
            file.write(line)
