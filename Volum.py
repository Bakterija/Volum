#!/usr/bin/env python
import pygame, os, find_sinks, subprocess
startup = True
def reset_sinks():
    global sink_list_index, sink_list, sink_count, sink_list_volume
    finds_main = find_sinks.main()
    sink_list = find_sinks.sec(finds_main)
    sink_count = int(len(sink_list) / 3)
    sink_list_index = sink_list[sink_count:-sink_count]
    sink_list_volume = sink_list[sink_count*2:]
    sink_list = sink_list[:sink_count]
    sink_list_volume = sink_list_index + sink_list_volume
    find_volume()
    if startup == True:
        print ('Available sinks: ', sink_list[:sink_count])
        print ('Volume: ', sink_list_volume)

def find_sink_index(sink_list_index):
    count = 0
    found = False
    for sinks in sink_list_index:
        b = sinks.find(str(sink))
        if b is not -1:
            found = True
            return count
        count+=1
    if found == False:
        print ("WARNING: Couldn't find the saved sink, switching to sink 0")
        global sink
        sink = 0
        find_sinks.write_settings('default_sink',sink)
        return 0

def find_volume():
    global volume
    count = 0
    for numbers in sink_list_volume[:sink_count]:
        b = numbers.find(str(sink))
        if b is not -1:
            volume = sink_list_volume[count+sink_count]
            volume = int(volume)
        count += 1

pygame.init()
pygame.display.set_caption('Volume')
icon = pygame.image.load('load/volum.png')
pygame.display.set_icon(icon)
sink = int(find_sinks.read_settings('default_sink = '))
scx = int(find_sinks.read_settings('X_window_size = '))
scy = int(find_sinks.read_settings('Y_window_size = '))
Display = pygame.display.set_mode((scx,scy))
print ('-------------------- Loading ------------------------')
print ('Surface size is: ', scx,'x', scy)
reset_sinks()
sink_index = int(find_sink_index(sink_list_index))
print ('Default sink: ', sink_list[sink_index])
eq_pic = pygame.image.load('load/eqpic.png')
eq_pic_hov = pygame.image.load('load/eqpic_hov.png')
##options_pic = pygame.image.load('load/optionspic.png')
##options_pic_hov = pygame.image.load('load/optionspic_hov.png')
clock = pygame.time.Clock()
volume = 50
find_volume()

white = (255,255,255)
grey = (235,235,235)
greyer = (225,225,225)
greyest =(215,215,215)
red = (255,100,100)
dark_red = (180,25,25)
dark_red2 = (220,70,70)
black = (0,0,0)
dark = (35,35,35)
ldark = (55,55,55)
blue = (80,80,150)
dblue = (50,50,120)
lblue = (130,130,220)
llblue = (180,180,245)
green = (0,255,0)
blgr = (34,67,79)
yellow = (200,200,120)

## Switch colors
##black = greyer
##white = yellow
##greyest = ldark
##grey = dark
##red = dark_red2


def draw_picture(x,y,picture):
    Display.blit(picture,(x,y))
    
def draw_text(text,variable,x,y,size,color,font):
    if font == 1:
        font_path = ('load/font.ttf')
    else:
        font_path = ('load/font2.ttf')
    font = pygame.font.Font(font_path,size)
    text = font.render((text + str(variable)), True, color)
    Display.blit(text, (x,y))

def draw_bar(bar_x, bar_y, bar_w, bar_h, color):  
    pygame.draw.rect(Display, color, [bar_x, bar_y, bar_w, bar_h])

def check_mouse_hover(x_list,m_pos,redraw,hover_var,custom_xlen):
    for obs in x_list:
        if obs[hover_var] == True:
            if custom_xlen == False:
                custom_xlen2 = obs[2]
            else:
                custom_xlen2 = custom_xlen
            if m_pos[0] > obs[0]+custom_xlen2 or m_pos[0] < obs[0] or m_pos[1] < obs[1] or m_pos[1] > obs[1]+obs[3]:
                obs[hover_var] = False
                redraw = True
    for obs in x_list:
        if obs[hover_var] == False:
            if custom_xlen == False:
                custom_xlen2 = obs[2]
            else:
                custom_xlen2 = custom_xlen
            if m_pos[0] < obs[0]+custom_xlen2 and m_pos[0] > obs[0]:
                if m_pos[1] < obs[1]+obs[3] and m_pos[1] > obs[1]:
                    obs[hover_var] = True
                    redraw = True
##    print (x_list)
    return x_list, redraw

def higher():
    global volume, volume_timer, reset_timer
    volume+=5
    if volume > 150:
        volume = 150
    volume_timer = reset_timer

def lower():
    global volume, volume_timer, reset_timer
    volume-=5
    if volume < 0:
        volume = 0
    volume_timer = reset_timer

def sys_arg_volum(volume):
    global sink
    volume = volume*655
    subprocess.Popen('pacmd set-sink-volume %s %s' % (sink, volume), shell=True,stdout=subprocess.PIPE)

def equalizer(equalizer_c):
    if equalizer_c == 'pulse-eq-gtk':
        os.system("pulseaudio-equalizer-gtk")
    elif equalizer_c == 'qpaeq':
        os.system("qpaeq")

def switch_sink_inputs(count,new_default):
    new_default = int(new_default)
    inputs_to_move = find_sinks.change_sink()
    os.system("load/./set_default_sink.sh %s" % (new_default))
    for inputs in inputs_to_move:
        os.system("load/./switch_inputs.sh %s %s" % (inputs[0],new_default))
    print ('Switched: ', inputs_to_move,' to ', sink_list[count])

def switch_sink_input(inputs,new_default):
    new_default = int(new_default)
    os.system("load/./switch_inputs.sh %s %s" % (inputs,sink_list_index[new_default]))
    print ('Switched: ', inputs,' to ', new_default)

def reset_inputs_list():
    #Pulse_Audio: index, media.name, volume%, sink_index, application.name
    input_list = find_sinks.change_sink()
    text_list = []
    bar_list = []
    bar_list2 = []
    bar_list3 = []
    offset = 0
    for inputs in input_list:
        offsetx = 0
        if len(inputs[4]) > 17:
            inputs[4] = inputs[4][:17] + '..'
        text_list.append(['',inputs[4],40,40+offset,16,black,2])
        bar_list.append([199,39+offset,120*1.5+2,15+2,black])
        bar_list2.append([200,40+offset,inputs[2]*1.5,15,red,0])
        for sinks in sink_list:
            text_list.append(['',sinks[:2],400+offsetx,40+offset,16,black,2])
            offsetx+=25
        offset += 30
    offset, offsetx, count = 0, 0, 0
    for inputs in input_list:
        for sinks in sink_list:
            if int(inputs[3]) == int(sink_list_index[count]):
                bar_list3.append([398+offsetx,38+offset,24,22,lblue,0,inputs[0],inputs[3]])
            else:
                bar_list3.append([398+offsetx,38+offset,24,22,lblue,0,inputs[0],-1])
            count +=1
            offsetx += 25
        offset += 30
        offsetx, count = 0, 0
##    print (input_list)
    return input_list, text_list, bar_list, bar_list2, bar_list3

def switch_sink(sink_list_index,num,moving_inputs):
    print ("Default sink set to ",sink_list_index)
    sink = sink_list_index
    sink_index = num
    if moving_inputs == True:
        switch_sink_inputs(num,sink)
    find_sinks.write_settings('default_sink',sink)
    reset_sinks()
    return sink, sink_index

def set_input_volume(index,volume):
    volume = volume*655
    subprocess.Popen('pacmd set-sink-input-volume %s %s' % (index, volume), shell=True,stdout=subprocess.PIPE)
        
def main_loop():
    global volume, volume_timer, reset_timer, sink, sink_list, sink_list_index, sink_count, startup
    reset_timer = int(find_sinks.read_settings('timer = '))
    moving_inputs = int(find_sinks.read_settings('m_inputs = '))
    sink_index = int(find_sink_index(sink_list_index))
    ##Button_list: 0X, 1Y, 2xlen, 3ylen, 4color, 5color_hover, 6command, 7hover
    button_list = [[38, 10, 56, 20, grey, llblue, 'Global::', False,14],[100, 10, 76, 20, grey, llblue, 'Programs::', False,14]]
    mouse_pos = pygame.mouse.get_pos()
    button_list[0][4], button_list[1][4] = greyest, grey
    check_equalizer = '0'
    if reset_timer < 0:
        reset_timer = 0
    inputs = find_sinks.change_sink()
    if startup == True:
        print ('Inputs: ', inputs)
        print ('Moving inputs: ', moving_inputs)
        if os.path.exists('/usr/bin/qpaeq') == True:
            check_equalizer = 'qpaeq'
        if os.path.exists('/usr/local/bin/qpaeq') == True:
            check_equalizer = 'qpaeq'
        if os.path.exists('/usr/bin/pulseaudio-equalizer-gtk') == True:
            check_equalizer = 'pulse-eq-gtk'
        if os.path.exists('/usr/local/bin/pulseaudio-equalizer-gtk') == True:
            check_equalizer = 'pulse-eq-gtk'
        if check_equalizer == '0' :
            print 'Equalizer not found'
        else:
            print check_equalizer,'found'
        print ('----------------------- Done ------------------------>')
        startup = False
    sink_reset_timer = 60
    redraw = True
    eq_hov = False
    eq_draw = eq_pic
    volume_timer = -9001
    oldsinks = find_sinks.main()
    newsinks = find_sinks.main()
    reset_sinks()
    while True:
        if volume_timer > 0:
            volume_timer -= 1
        if sink_reset_timer > 0:
            sink_reset_timer -= 1
        else:
            oldsinks = list(newsinks)
            newsinks = find_sinks.main()
            sink_reset_timer = 60
            if newsinks != oldsinks:
                reset_sinks()
                redraw = True
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and volume<150:
                    higher()
                    redraw = True
                if event.key == pygame.K_a and volume>0:
                    lower()
                    redraw = True
                if event.key == pygame.K_RIGHT and volume<150:
                    higher()
                    redraw = True     
                if event.key == pygame.K_LEFT and volume>0:
                    lower()
                    redraw = True
                if event.key == pygame.K_F2:
                    program_loop(button_list)
                if event.key == pygame.K_e:
                    stop = False
                    if moving_inputs == 0:
                        moving_inputs = 1
                        stop = True
                        print ('Moving inputs')
                    if moving_inputs == 1 and stop == False:
                        moving_inputs = 0
                        print ('Not moving inputs')
                    find_sinks.write_settings('m_inputs',moving_inputs)
                    redraw = True
                if event.key == pygame.K_1:
                    if sink_count > 0:
                        sink, sink_index = switch_sink(sink_list_index[0],0,moving_inputs)
                        find_volume()
                        redraw = True
                if event.key == pygame.K_2:
                    if sink_count > 1:
                        sink, sink_index = switch_sink(sink_list_index[1],1,moving_inputs)
                        find_volume()
                        redraw = True
                if event.key == pygame.K_3:
                    if sink_count > 2:
                        sink, sink_index = switch_sink(sink_list_index[2],2,moving_inputs)
                        find_volume()
                        redraw = True
                if event.key == pygame.K_4:
                    if sink_count > 3:
                        sink, sink_index = switch_sink(sink_list_index[3],3,moving_inputs)
                        find_volume()
                        redraw = True
                if event.key == pygame.K_5:
                    if sink_count > 4:
                        sink, sink_index = switch_sink(sink_list_index[4],4,moving_inputs)
                        find_volume()
                        redraw = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    higher()
                    redraw = True
                if event.button == 5:
                    lower()
                    redraw = True
                elif event.button == 1:
                    if check_equalizer is not 0:
                        if mouse_pos[0] < scx/12.5+64 and mouse_pos[0] > scx/12.5:
                            if mouse_pos[1] < scy/1.5+64 and mouse_pos[1] > scy/1.5:
                                equalizer(check_equalizer)
                                redraw = True
                    if mouse_pos[0] < scx/3.57 and mouse_pos[0] > scx/12.5:
                            if mouse_pos[1] < scy/3 and mouse_pos[1] > scy/3.75+4:
                                reset_sinks()
                                redraw = True
                                
                    for x in button_list:
                        if x[7] == True:
                            if x[6] == 'Global::':
                                main_loop()
                            if x[6] == 'Programs::':
                                program_loop(button_list)

            button_list, redraw = check_mouse_hover(button_list,mouse_pos,redraw,7,False)
            if mouse_pos[0] < scx/12.5+64 and mouse_pos[0] > scx/12.5:
                if mouse_pos[1] < scy/1.5+64 and mouse_pos[1] > scy/1.5:
                    eq_draw = eq_pic_hov
                    redraw = True
                    eq_hov = True            

            if eq_hov == True:
                if mouse_pos[0] > scx/12.5+48 or mouse_pos[0] < scx/12.5 or mouse_pos[1] > scy/1.5+48 or mouse_pos[1] < scy/1.5:
                    eq_draw = eq_pic
                    redraw = True
                    eq_hov = False
                  
        if volume_timer == 0:
            volume_timer -= 9001
            sys_arg_volum(volume)
                    
        if redraw == True:
            Display.fill(grey)

            draw_bar(scx/12.5-2,scy/7.5-2,150*scx/178.571+4,scy/10+4,black)
            if volume <105:
                draw_bar(scx/12.5,scy/7.5,volume*scx/178.571,scy/10,red)
            if volume > 100:
                draw_bar(scx/12.5,scy/7.5,100*scx/178.571,scy/10,red)
                draw_bar(scx/12.5+100*scx/178.571,scy/7.5,(volume-100)*scx/178.571,scy/10,blue)
            draw_text('',volume,scx/12.5+5,scy/7.5+2,22,white,1)
            if moving_inputs == True:
                draw_text('Sink: ',sink_list[sink_index],scx/12.5+2,scy/3.75+2,18,black,2)
            else:
                draw_text('Sink: ',sink_list[sink_index],scx/12.5+2,scy/3.75+2,18,dark_red,2)
            for x in button_list:
                if x[7] == True:
                    draw_bar(x[0],x[1],x[2],x[3],x[5])
                else:
                    draw_bar(x[0],x[1],x[2],x[3],x[4])
                draw_text(x[6],'',x[0]+3,x[1]+2,x[8],black,2)
            
            if check_equalizer is not 0:
                draw_picture(scx/12.5,scy/1.5,eq_draw)
                    
            pygame.display.update()
            redraw = False
            
        clock.tick(60)

def program_loop(button_list):
    global volume_timer, reset_timer, sink, sink_list, sink_list_index, sink_count
    input_list, text_list, bar_list,bar_list2, bar_list3 = reset_inputs_list()
    button_list[0][4], button_list[1][4] = grey, greyest
    ##Bar lists: 0X, 1Y, 2Width, 3Height, 4Color, 5Hover)
    bar2 = 120*1.5
    bar3 = 22
    mouse_pos = [0,0]
    moved_pixels = 0
    input_reset_timer = 60
    redraw = True
    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
                
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    main_loop()
                if event.key == pygame.K_r:
                    input_list, text_list, bar_list,bar_list2, bar_list3 = reset_inputs_list()
                    redraw = True
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    count, move = 0, 1
                    for bar in bar_list2:
                        if bar[5] == 1:
                            move = 0
                            if input_list[count][2] < 120:
                                input_list[count][2] += 5
                                if input_list[count][2] > 120:
                                    input_list[count][2] = 120
                                bar[2] = input_list[count][2]*1.5
                                set_input_volume(input_list[count][0],input_list[count][2])
                        count += 1
                    if move == 1 and moved_pixels < 0:
                        for bar in bar_list:
                            bar[1] += 10
                        for bar in bar_list2:
                            bar[1] += 10
                        for bar in bar_list3:
                            bar[1] += 10
                        for text in text_list:
                            text[3] += 10
                        moved_pixels += 1
                    redraw = True
                if event.button == 5:
                    count, move = 0, 1
                    for bar in bar_list2:
                        if bar[5] == 1:
                            move = 0
                            if input_list[count][2] > 0:
                                input_list[count][2] -= 5
                                if input_list[count][2] < 0:
                                    input_list[count][2] = 0
                                bar[2] = input_list[count][2]*1.5
                                set_input_volume(input_list[count][0],input_list[count][2])
                        count += 1
                    if move == 1:
                        for bar in bar_list:
                            bar[1] -= 10
                        for bar in bar_list2:
                            bar[1] -= 10
                        for bar in bar_list3:
                            bar[1] -= 10
                        for text in text_list:
                            text[3] -= 10
                        moved_pixels -= 1
                    redraw = True
                elif event.button == 1:
                    for x in button_list:
                        if x[7] == True:
                            if x[6] == 'Global::':
                                main_loop()
                            if x[6] == 'Programs::':
                                program_loop(button_list)
                    count = 0
                    for bar in bar_list3:
                        if bar[5] == 1:
                            if bar[0] == 398:
                                switch_sink_input(int(bar[6]),0)
                            if bar[0] == 398+25:
                                switch_sink_input(int(bar[6]),1)
                            if bar[0] == 398+50:
                                switch_sink_input(int(bar[6]),2)
                            input_list, text_list, bar_list,bar_list2, bar_list3 = reset_inputs_list()
                            redraw = True

            ## 0x_list, 1m_pos, 2redraw, 3hover_var, 4custom_xlen
            bar_list2, redraw = check_mouse_hover(bar_list2,mouse_pos,redraw,5,bar2)
            bar_list3, redraw = check_mouse_hover(bar_list3,mouse_pos,redraw,5,bar3)
            button_list, redraw = check_mouse_hover(button_list,mouse_pos,redraw,7,False)
                        
        if redraw == True:
            Display.fill(grey)
            ## Under Volume bars
            for bar in bar_list:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],bar[4])
            ## Volume bars
            for bar in bar_list2:
                if bar[5] == 0:
                    if bar[2] > 150:
                        draw_bar(bar[0],bar[1],150,bar[3],bar[4])
                        draw_bar(bar[0]+150,bar[1],bar[2]-150,bar[3],blue)
                    else:
                        draw_bar(bar[0],bar[1],bar[2],bar[3],bar[4])
                else:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],blue)
                draw_text('',int(bar[2]/1.5),bar[0]+5,bar[1]+1,12,white,1)
            ## Device buttons
            for bar in bar_list3:
                if bar[7] > -1:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],green)
                if bar[7] == -1:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],bar[4])
                if bar[5] == 1:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],red)
            for text in text_list:
                draw_text(text[0],text[1],text[2],text[3],text[4],text[5],text[6])
            draw_bar(0,0,scx,scy/8,grey)
            for x in button_list:
                if x[7] == True:
                    draw_bar(x[0],x[1],x[2],x[3],x[5])
                else:
                    draw_bar(x[0],x[1],x[2],x[3],x[4])
                draw_text(x[6],'',x[0]+3,x[1]+2,x[8],black,2)
            redraw = False
            pygame.display.update()
            
        clock.tick(60)
        
main_loop()
pygame.quit()
quit()
