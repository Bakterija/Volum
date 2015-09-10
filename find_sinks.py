#!/usr/bin/env python
import os
path = os.getcwd()+'/'

def output_sinks():
    os.system("load/./devices.sh %s" % (path+('load/sinks.txt')))

def readf(filename):
    file = path+filename
    f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

def editf(a):
    count = 0
    newlist = []
    for lines in a:
        b = lines.find('alsa.name')
        if b is not -1:
            newlist.append(a[count])
        else:
            b = lines.find('FFT based equalizer')
            if b is not -1:
                newlist.append('alsa.name = "FFT equalizer"')
        count+=1
    count = 0
    for lines in newlist:
        b = lines.find('alsa')
        lines = lines[b:]
        newlist[count] = lines
        count+=1
    count = 0
    for lines in a:
        b = lines.find('index:')
        if b is not -1:
            newlist.append('index = "' + lines[b+7:] + '"')
        count+=1
    return newlist

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
    newlist = []
    for lines in text:
        b = lines.find('index:')
        if b is not -1:
            newlist.append(lines[b+7:])
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

def main():
    output_sinks()
    a = readf('load/sinks.txt')
    a = editf(a)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/sinks.txt')

def sec():
    text = readf('load/sinks.txt')
    sinklist = []
    for lines in text:
        b = lines.find('=')
        if b is not -1:
            c = lines[b+3:-1]
            sinklist.append(c)
    return sinklist

def change_sink():
    os.system("load/./get_inputs.sh")
    text = readf('load/inputs.txt')
    text = edit_inputs_file(text)
##    text = a = '\n'.join(str(e) for e in a)
##    savef(text,'load/inputs.txt')
    return text

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
