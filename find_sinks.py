#!/usr/bin/env python
import os, subprocess
path = os.getcwd()+'/'

def readf(filename):
    file = path+filename
    f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

def editf(a):
    li_count = 0
    index = -1
    newlist = []
    ## 0index, 1volume, 2name
    newlist2 = []
    for lines in a:
        b = lines.find('index:')
        if b is not -1:
            newlist.append([lines[b+7:]])
            newlist2.append([lines[b+7:]])
    for lines in a:
        b = lines.find('index:')
        if index > -1:
            newlist[index].append(lines)
        if b is not -1:
            index += 1
    index = 0
    for indexes in newlist:
        for text in indexes:
            b = text.find('alsa.name')
            if b is not -1:
                newlist2[index].append(text[b+13:-1])
            b = text.find('volume:')
            if b is not -1:
                c = text.find('base volume:')
                if c is -1:
                    b = text.find('%')
                    newlist2[index].append(int(text[b-3:b]))
        index+=1
    count = 0
    for x in newlist2:
        if len(x) < 3:
##            newlist2.pop(count)
            newlist2[count].append('Noname')
        count+= 1
    count = 0
    for x in newlist2:
        x.append(count)
        count+= 1

    return newlist2

def edit_settings(text,text_find,new_value):
    count = 0
    newlist = []
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = text_find + ' = ' + str(new_value)
            newlist.append(c)
        else:
            newlist.append(lines)
        count+=1
    count = 1
    return newlist

def edit_inputs_file(text):
    app_index = []
    app_name = []
    app_volume = []
    app_sink_index = []
    newlist = []
    for lines in text:
        b = lines.find('index:')
        if b is not -1:
            app_index.append(lines[b+7:])
    for lines in text:
        b = lines.find('media.name')
        if b is not -1:
            app_name.append(lines[b+14:-1])
    for lines in text:
        b = lines.find('volume:')
        if b is not -1:
            c = lines.find('base volume:')
            if c is -1:
                b = lines.find('%')
                app_volume.append(int(lines[b-3:b]))
    for lines in text:
        b = lines.find('sink: ')
        if b is not -1:
            try:
                app_sink_index.append(int(lines[7:10]))
            except:
                app_sink_index.append(int(lines[7:9]))
    listlen = len(app_index)
    count = 0
    while count < listlen:
        b = app_name[count].find('Equalized Stream')
        if b is -1:
            newlist.append([app_index[count],app_name[count],int(app_volume[count]),int(app_sink_index[count])])
        count += 1
    count = 0
    for lines in text:
        b = lines.find('application.name = ')
        if b is not -1:
            newlist[count].append(lines[3+len('application.name = '):-1])
            count += 1
    return newlist

def get_settings(text,text_find):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    return c

def savef(text,file):
    f = open(path+file, 'w')
    f.write(text)
    f.close()

def read_sinks():
    INPUT = 'pacmd list-sinks'
    cmd_FORMAT = INPUT.split()
    output = subprocess.Popen(cmd_FORMAT, stdout=subprocess.PIPE).communicate()[0]
    output = str(output)
    output = output.splitlines()
    return output

def main():
    a = read_sinks()
    a = editf(a)
    return a

def change_sink():
    INPUT = 'pacmd list-sink-inputs'
    cmd_FORMAT = INPUT.split()
    output = subprocess.Popen(cmd_FORMAT, stdout=subprocess.PIPE).communicate()[0]
    text = str(output)
    text = output.splitlines()
    text = edit_inputs_file(text)
    return text

def get_input_list():
    INPUT = 'pacmd list-sink-inputs'
    cmd_FORMAT = INPUT.split()
    output = subprocess.Popen(cmd_FORMAT, stdout=subprocess.PIPE).communicate()[0]
    output = str(output)
    return output

def write_settings(text_find,new_value):
    a = readf('load/settings')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/settings')

def read_settings(text_find):
    a = readf('load/settings')
    a = get_settings(a,text_find)
    return a


main()
