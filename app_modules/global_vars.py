import os

bgg1 = '#DCDCDC'
window_bgcol = '#EBEBEB'
window_bgcol2 = '#C8C8C8'
vol_grey = "#%02x%02x%02x" % (235,235,235)
greyer = "#%02x%02x%02x" % (225,225,225)
greyest = "#%02x%02x%02x" % (215,215,215)
dark_red = "#%02x%02x%02x" % (180,25,25)
dark_red2 = "#%02x%02x%02x" % (220,70,70)
dark = "#%02x%02x%02x" % (35,35,35)
ldark = "#%02x%02x%02x" % (55,55,55)
vol_red = "#%02x%02x%02x" % (255,100,100)
vol_blue = "#%02x%02x%02x" % (80,80,150)
vol_red2 = "#%02x%02x%02x" % (215,70,70)
vol_blue2 = "#%02x%02x%02x" % (50,50,120)
dblue = "#%02x%02x%02x" % (50,50,120)
lblue = "#%02x%02x%02x" % (130,130,220)
llblue = "#%02x%02x%02x" % (180,180,245)
vol_green = "#%02x%02x%02x" % (0,255,0)
blgr = "#%02x%02x%02x" % (29,62,84)
blgr2 = "#%02x%02x%02x" % (14,47,59)
vol_yellow = "#%02x%02x%02x" % (200,200,120)
EQUALIZER = None

if os.path.exists('/usr/bin/qpaeq') == True:
    EQUALIZER = 'qpaeq'
elif os.path.exists('/usr/local/bin/qpaeq') == True:
    EQUALIZER = 'qpaeq'
elif os.path.exists('/usr/bin/pulseaudio-equalizer-gtk') == True:
    EQUALIZER = 'pulse-eq-gtk'
elif os.path.exists('/usr/local/bin/pulseaudio-equalizer-gtk') == True:
    EQUALIZER = 'pulse-eq-gtk'
if EQUALIZER:
    print ('Found equalizer: %s' % EQUALIZER)
else:
    print ('Equalizer not found')
