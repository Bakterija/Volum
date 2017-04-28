def readf(filename):
    file = filename
    try:
        f = open(file, 'rU')
    except:
        savef('',filename)
        f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

def savef(text,file):
    f = open(file, 'w')
    f.write(text)
    f.close()

def edit_settings(text,text_find,new_value):
    count = 0
    newlist = []
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = text_find + '=' + str(new_value)
            newlist.append(c)
        else:
            newlist.append(lines)
        count+=1
    count = 1
    return newlist

def read_settings(*arg):
    a = readf('load/settings.ini')
    a = get_settings(a,arg[0],arg[1])
    return a

def get_settings(text,text_find,default_value):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    ## Checks if it exists and appends something, if not
    try:
        if c == '':
            c = default_value
            if default_value != '':
                write_settings(text_find[:-1],'\n'+c)
    except:
        c = default_value
        fh = open('load/settings.ini', 'a')
        fh.write('\n'+str(text_find)+str(c))
        fh.close()
    return c

def write_settings(text_find,new_value):
    a = readf('load/settings.ini')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/settings.ini')
