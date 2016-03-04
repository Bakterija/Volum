#!/usr/bin/env python
import os
import getpass

user = getpass.getuser()
path = os.getcwd()+'/'

def editf():
    a = []
    a.append('[Desktop Entry]')
    a.append('Comment=')
    a.append('Terminal=false')
    a.append('Name=sPAGUI')
    a.append('Exec='+ path + 'sPAGUI.py')
    a.append('Path='+ path)
    a.append('Type=Application')
    a.append('Icon=' + path + 'load/icon.ico')
    return a

def savef(text):
    f = open('/home/'+ user + '/Desktop/sPAGUI.desktop', 'w')
    print ('/home/'+ user + '/Desktop/sPAGUI.desktop')
    f.write(text)
    f.close()

def main():
    file = editf()
    text = file = '\n'.join(str(e) for e in file)
    savef(text)
    print('------->')
    print('Done!')


main()
