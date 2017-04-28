#!/bin/bash
## Source http://www.webupd8.org/2013/03/install-pulseaudio-with-built-in-system.html


wget http://cgit.freedesktop.org/pulseaudio/pulseaudio/plain/src/utils/qpaeq -O /tmp/qpaeq
sudo install /tmp/qpaeq /usr/local/bin/

sudo apt-get install python-dbus python-qt4 python-qt4-dbus pulseaudio-utils

pulseaudio -k

pulseaudio &

sleep 1

pactl load-module module-equalizer-sink

pactl load-module module-dbus-protocol
