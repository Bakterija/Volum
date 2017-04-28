from . pyver import PY3
import subprocess


class PAController:
    def __init__(self):
        print ('-'*21+'PAController __init__'+'-'*21+'\n'+'-'*64)
        self.reload_gui = False
        self.startup = True
        self.sink_inputs2, self.sinks2 = [], []
        self.reset_sinks_inputs()
        self.reset_sinks_inputs()

    def return_sinks(self):
        return self.sinks

    def return_inputs(self):
        return self.sink_inputs

    def reset_sinks_inputs(self):
        if self.reload_gui == False:
            if self.startup == False:
                self.sink_inputs2, self.sinks2 = self.sink_inputs, self.sinks
            self.sink_inputs = subprocess_return('pacmd list-sink-inputs')
            self.sink_inputs = self.sink_inputs.split('\n')
            self.sink_inputs = self.get_sink_inputs(self.sink_inputs)
            if self.startup == True:
                print('[index]  [media.name]  [volume]  [sink]  [application.name]')
                for x in self.sink_inputs:
                    print (
                        '[%s - %s - %s - %s - %s]' % (
                        x[0], x[1], x[2], x[3], x[4]))
                print ('-'*64+'\n'+'-'*64)
            self.sinks = subprocess_return('pacmd list-sinks')
            self.sinks = self.sinks.splitlines()
            self.sinks = self.get_sinks(self.sinks)
            if self.startup == True:
                print ('[index]  [volume] [alsa.name]  [application.name]')
                for x in self.sinks:
                    print ('[%s - %s - %s - %s]' % (x[0], x[1], x[2], x[3]))
                print ('-'*64+'\n'+'-'*64)
            if self.sink_inputs != self.sink_inputs2 or self.sinks != self.sinks2:
                self.reload_gui = True
            if self.startup == True:
                self.startup = False

    def get_sinks(self,a):
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
                newlist2[count].append('Noname')
            count+= 1
        count = 0
        for x in newlist2:
            x.append(count)
            count+= 1
        return newlist2

    def get_sink_inputs(self,a):
        li_count = 0
        index = -1
        app_index = []
        app_name = []
        app_volume = []
        app_sink_index = []
        newlist = []
        newlist2 = []
        templist = []
        for lines in a:
            b = lines.find('index:')
            if b is not -1:
                newlist.append([lines[b+7:]])
                newlist2.append([lines[b+7:]])
        for lines in a:
            b = lines.find('index:')
            if index > -1:
                newlist[index].append(lines)
            if b != -1:
                index += 1
        index = 0
        for indexes in newlist:
            media_name,app_volume,app_sink,app_name = 'n/a','n/a','n/a','n/a'
            for lines in indexes:
                b = lines.find('media.name')
                if b is not -1:
                    media_name = lines[b+14:-1]
                b = lines.find('volume:')
                if b is not -1:
                    c = lines.find('base volume:')
                    if c is -1:
                        b = lines.find('%')
                        app_volume = int(lines[b-3:b])
                b = lines.find('sink: ')
                if b is not -1:
                    try:
                        app_sink = int(lines[b+6:b+9])
                    except:
                        app_sink = int(lines[b+6:b+8])
                b = lines.find('application.name = ')
                if b is not -1:
                    app_name = lines[3+len('application.name = '):-1]
            newlist2[index].append(media_name)
            newlist2[index].append(app_volume)
            newlist2[index].append(app_sink)
            newlist2[index].append(app_name)
            index+= 1
        return newlist2


def subprocess_return(INPUT):
        cmd_FORMAT = INPUT.split()
        output = subprocess.Popen(
            cmd_FORMAT, stdout=subprocess.PIPE).communicate()[0]
        if PY3:
            output = output.decode('utf-8')
        else:
            output = str(output)
        return output
