#!/usr/bin/env python
import os


path = os.getcwd()+'/'
os.system("load/./devices.sh %s" % (path+('/sinks.txt')))

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
    newlist.append(a[1])
    for lines in a:
        b = lines.find('alsa.name')
        if b is not -1:
            newlist.append(a[count])
        count+=1
    count = 1
    for lines in newlist[1:]:
        b = lines.find('alsa')
        lines = lines[b:]
        newlist[count] = lines
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
    a = readf('sinks.txt')
    a = editf(a)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'sinks.txt')

def sec():
    text = readf('sinks.txt')
    sinklist = []
    for lines in text:
        b = lines.find('=')
        if b is not -1:
            c = lines[b+3:-1]
            sinklist.append(c)
    return sinklist

def write_settings(text_find,new_value):
    a = readf('settings')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'settings')

def read_settings(text_find):
    a = readf('settings')
    a = get_settings(a,text_find)
    return a


main()
