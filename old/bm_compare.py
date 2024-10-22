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

def GetHeaderIndent(line):
    result=re.subn('^([ ]*)<DT><H3.*$','\\1',line)
    return None if result[1] == 0 else len(result[0])//4

# line="""<DT><H3 ADD_DATE="1629716476" LAST_MODIFIED="1629716476">New folder</H3>"""
# print(GetHeaderIndent(line))

input_file_names = getFilesInDir('input')

# for i in input_file_names:
#     print(i)

dups = dict()
input_files_lines=[]

for file_name in input_file_names:
    lines=ReadFileLines(file_name)
    lines2 = []
    channel_link_count = 0

    for line in lines:
        channelId = GetLinkChannelID(line)

        if channelId == None:
            if IsNotChannelLink(line):
                lines2.append(line)

            continue

        if channelId not in dups:
            dups[channelId]=0

        if dups[channelId] == 0:
            lines2.append(line)
            channel_link_count+=1

        dups[channelId]+=1

    lines2 = lines2 if channel_link_count > 0 else []
    input_files_lines.append(lines2)


for i,file_name in enumerate(input_file_names):
    lines = input_files_lines[i]

    last_header_indent = 0
    last_header_index = -1
    header_channel_count=0

    for j,line in enumerate(lines):
        channelId = GetLinkChannelID(line)

        if channelId != None:
            header_channel_count+=1
        else:
            if IsNotChannelLink(line):
                header_indent = GetHeaderIndent(line)

                if header_indent != None:
                    if header_indent <= last_header_indent:
                        if last_header_index != -1 and header_channel_count == 0:
                            lines[last_header_index] = ''

                    # lines[j]+= '<p>poo c={}</p>'.format(header_channel_count)
                    last_header_indent = header_indent
                    last_header_index = j
                    header_channel_count=0

for i in range(0,len(input_file_names)):
    input_file_name=input_file_names[i]
    input_file_lines= input_files_lines[i]

    output_file_name=re.sub('input(.*)','output\\1',input_file_name)
    output_file_name=fixFileName(output_file_name)

    if len(input_file_lines) == 0:
        continue

    # print(input_file_name)
    print(output_file_name)

    with open(output_file_name, "w", encoding='utf-8') as file:
        for line in input_file_lines:
            file.write(line)
