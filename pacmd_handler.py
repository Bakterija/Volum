# Includes parseList function from https://github.com/avindra/pacmd-python
from subprocess import PIPE, Popen
from sys import argv
import json
import re

def shell_exec(cmd):
    """Returns tuple with stdout, stderr"""
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')
    return out, err

def parseList(output):
    lines = output.split('\n')
    first = lines.pop(0)

    if first.startswith('Unknown command'):
        raise Exception(first)

    data = {'sink indexes': []}

    currentItem = {}
    currentIndex = -1

    patternNewItem = re.compile('(\* )?index: (\d+)')
    patternKeyValue = re.compile('\t*([^:]+):(?: (.+))?')
    patternEnumerating = re.compile('^\tproperties:')
    patternProps = re.compile('(\S+) = "(.+)"')

    enumeratingProps = None

    lastKey = None

    for line in lines:
        matchNewItem = patternNewItem.search(line)
        matchKeyValue = patternKeyValue.search(line)
        matchEnumerating = patternEnumerating.search(line)


        if enumeratingProps:
            matchProps = patternProps.search(line)
            if matchProps:
                enumeratingProps[matchProps.group(1)] = matchProps.group(2)
                continue
            else: # reset
                currentItem['properties'] = enumeratingProps
                enumeratingProps = None

        if matchEnumerating:
            enumeratingProps = { 'device-api' : None }
        elif matchNewItem:
            isActive = matchNewItem.group(1) == '* '
            index = matchNewItem.group(2)

            # Finalize object and reset
            if currentIndex != -1:
                data[currentIndex] = currentItem
                currentItem = {}

            currentIndex = index
            data['sink indexes'].append(index)

            if isActive:
                data['active sink'] = index

        elif matchKeyValue:
            parsedKey = matchKeyValue.group(1).strip()
            parsedValue = matchKeyValue.group(2)

            # skip until we're out of "ports".
            # not currently supported
            if lastKey == 'ports' and parsedKey != 'active port':
                continue

            lastKey = parsedKey
            currentItem[parsedKey] = parsedValue
        elif lastKey and lastKey != 'ports':
            # If it gets to here, we can assume its a multiline attr
            currentItem[lastKey] += re.sub('^\s+', '\n', line)

    # Last item will need to be pushed manually
    data[currentIndex] = currentItem

    # Update volume 
    for k in data['sink indexes']:
        currentItem = data[k]

        cnt = currentItem['base volume'].count('/')
        if cnt == 2:
            currentItem['base volume items'] = ['value', 'percent', 'db']
        elif cnt == 1:
            currentItem['base volume items'] = ['value', 'percent']

        voldict = {}
        text = currentItem['volume']
        text = text.replace('\n', '/')
        text = text.replace(' ', '/')
        text = re.split(' / |\s|\n', currentItem['volume'])
        text = list(filter(None, text))
        for i in range(len(text)):
            if text[i][-1] == ',':
                text[i] = text[i][:-1]
        vol_i = 0
        while vol_i < len(text):
            if (text[vol_i][-1] == ':'):
                vol_key = text[vol_i][:-1]
                voldict[vol_key] = {}
                for x in currentItem['base volume items']:
                    voldict[vol_key][x] = text[vol_i+1]
                    vol_i += 1
            if (text[vol_i] == 'balance'):
                voldict['balance'] = text[vol_i+1]
                vol_i += 1
            vol_i += 1
            currentItem['volume'] = voldict

    return data


def parse_sink_inputs(text):
    li_count = 0
    index = -1

    newlist = []
    newlist2 = []
    text = text.splitlines()
    for lines in text:
        b = lines.find('index:')
        if b is not -1:
            newlist.append([lines[b+7:]])
            newlist2.append([lines[b+7:]])
    for lines in text:
        b = lines.find('index:')
        if index > -1:
            newlist[index].append(lines)
        if b != -1:
            index += 1
    index = 0
    for indexes in newlist:
        media_name = ''
        app_volume = ''
        app_sink = ''
        app_name = ''
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


def get_sinks():
    result = {}
    cmd = ['pacmd', 'list-sinks']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    res = p.communicate()[0]
    res = res.decode('utf-8')
    pa_info_dict = parseList(res)
    result['active sink'] = pa_info_dict['active sink']
    result['sink indexes'] = pa_info_dict['sink indexes']
    result['sinks'] = {}
    # result['sink indexes']
    for k in pa_info_dict['sink indexes']:
        result['sinks'][k] = pa_info_dict[k]
    return result

def get_sink_inputs():
    result = {}
    cmd = ['pacmd', 'list-sink-inputs']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    res = p.communicate()[0]
    res = res.decode('utf-8')
    sink_input_list = parse_sink_inputs(res)
    
    result['sink inputs'] = {}
    result['sink input indexes'] = []
    for x in sink_input_list:
        result['sink input indexes'].append(x[0])
        result['sink inputs'][x[0]] = {
            'index': x[0], 'media name': x[1], 'volume': x[2],
            'sink': x[3], 'app name': x[4]
        }
    return result

def set_input_volume(index, volume):
    volume = volume * 655
    Popen(
        'pacmd set-sink-input-volume %s %s' % (index, volume),
        shell=True, stdout=PIPE)

def set_sink_volume(index, volume):
    volume = int(volume) * 655
    cmd = ['pacmd', 'set-sink-volume', str(index), str(volume)]
    res = shell_exec(cmd)
    if res[0].find('No sink found by this name') != -1:
        raise Exception(res[0])

def move_sink_input(index, new_sink, set_volume=None):
    Popen(
        'pacmd move-sink-input %s %s' % (index, new_sink),
        shell=True, stdout=PIPE)
    if set_volume:
        time.sleep(0.05)
        set_input_volume(index, set_volume)

def move_inputs_to_sink(index):
    res = get_inputs()
    Popen(
        "pacmd set-default-sink %s" % (index),
        shell=True, stdout=PIPE)
    if not res['sink inputs']:
        return

    for k, v in res['sink inputs'].items():
        move_sink_input(k, index, v['volume'])


if __name__ == '__main__':
    result = {}
    if 'sinks' in argv:
        result.update(get_sinks())

    if 'sink-inputs' in argv:
        result.update(get_sink_inputs())

    if 'nice-format' in argv:
        print(json.dumps(result, sort_keys=True, indent=4))
    else:
        print(json.dumps(result))
