#!/usr/bin/env python
import os
maxvol = 150*655

def output_sinks():
    elo = os.popen("pacmd list-sinks")
    elo = list(elo)
    return elo

def editf(a):
    count = 0
    newlist = []
    for lines in a:
        b = lines.find('index:')
        if b is not -1:
            newlist.append(int(lines[b+7:]))
            count+=1
    for lines in a:
        b = lines.find('volume:')
        if b is not -1:
            c = lines.find('base volume:')
            if c is -1:
                b = lines.find('%')
                if int(lines[b-3:b]) < 100:
                    newlist.append(int(lines[b-2:b]))
                else:
                    newlist.append(int(lines[b-3:b]))
    return newlist


def main():
    a = output_sinks()
    sink_list = editf(a)
    sink_count = int(len(sink_list) / 2)
    sink_list_index = sink_list[:sink_count]
    sink_list_volume = sink_list[sink_count:]
    count = 0
    for sinks in sink_list_index:
        if sink_list_volume[count] > 0:
            sink_list_volume[count] = int(sink_list_volume[count])
            sink_list_volume[count] = sink_list_volume[count]*655-3275
            if sink_list_volume[count] < 0:
                sink_list_volume[count] = 0
            os.popen('pacmd set-sink-volume %s %s' % (sinks, sink_list_volume[count]))
        count +=1



main()
