#!/usr/bin/env python
import pygame, sys, os, subprocess, find_sinks
def reset_sinks():
    global sink_list_index, sink_list, sink_count
    find_sinks.main()
    sink_list = find_sinks.sec()
    print ('Available sinks: ', sink_list)
    sink_count = int(len(sink_list) / 2)
    sink_list_index = sink_list[sink_count:]
    sink_list = sink_list[:sink_count]

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

pygame.init()
pygame.display.set_caption('Volum')
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

white = (255,255,255)
grey = (235,235,235)
red = (255,100,100)
dark_red = (180,25,25)
black = (0,0,0)
dark = (35,35,35)
blue = (80,80,150)
lblue = (130,130,220)
green = (0,255,0)
blgr = (34,67,79)


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

def higher():
    global volume, volume_timer, reset_timer
    volume+=5
    volume_timer = reset_timer

def lower():
    global volume, volume_timer, reset_timer
    volume-=5
    volume_timer = reset_timer

def sys_arg_volum(volume):
    global sink
    subprocess.call('pactl set-sink-volume %s %s' % (sink, volume)+("%"), shell=True)

def equalizer():
    os.system("load/./equalizer.sh")

def get_volume():
    komanda = subprocess.Popen(["amixer"], stdout=subprocess.PIPE)
    output = komanda.communicate()[0]
    output2 = output.decode('utf-8')
    output3 = output2.find('%')
    output4 = output2[output3-3:output3]
    output5 = output4.replace('[','')
    return int(output5)

def switch_sink_inputs(count,new_default):
    new_default = int(new_default)
    inputs_to_move = find_sinks.change_sink()
    os.system("load/./set_default_sink.sh %s" % (new_default))
    for inputs in inputs_to_move:
        os.system("load/./switch_inputs.sh %s %s" % (inputs[0],new_default))
    print ('Switched: ', inputs_to_move,' to ', sink_list[count])

def switch_sink_input(inputs,new_default):
    new_default = int(new_default)
    os.system("load/./switch_inputs.sh %s %s" % (inputs,new_default))
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
        if len(inputs[1]) > 15:
            inputs[1] = inputs[1][:15] + '..'
        text_list.append(['',inputs[4],40,40+offset,16,black,2])
        bar_list.append([199,39+offset,100*1.5+2,15+2,black])
        bar_list2.append([200,40+offset,inputs[2]*1.5,15,red,0])
        for sinks in sink_list:
            text_list.append(['',sinks[:2],400+offsetx,40+offset,16,black,2])
            offsetx+=25
        offset += 30
    offset, offsetx, count = 0, 0, 0
    for inputs in input_list:
        for sinks in sink_list:
            if inputs[3] == count:
                bar_list3.append([398+offsetx,38+offset,24,22,lblue,0,inputs[0],inputs[3]])
            else:
                bar_list3.append([398+offsetx,38+offset,24,22,lblue,0,inputs[0],-1])
            count +=1
            offsetx += 25
        offset += 30
        offsetx, count = 0, 0
    return input_list, text_list, bar_list, bar_list2, bar_list3

def set_input_volume(index,volume):
    volume = volume*655
    os.popen('pacmd set-sink-input-volume %s %s' % (index, volume))

        
def main_loop():
    global volume, volume_timer, reset_timer, sink, sink_list, sink_list_index, sink_count
    reset_timer = int(find_sinks.read_settings('timer = '))
    moving_inputs = int(find_sinks.read_settings('m_inputs = '))
    sink_index = int(find_sink_index(sink_list_index))
    mouse_pos = pygame.mouse.get_pos()
    if reset_timer < 0:
        reset_timer = 0
    check_equalizer = os.path.exists('/usr/bin/qpaeq')
    if check_equalizer == False:
        check_equalizer = os.path.exists('/usr/local/bin/qpaeq')
    inputs = find_sinks.change_sink()
    print ('Inputs: ', inputs)
    print ('Moving inputs: ', moving_inputs)
    print ('----------------------- Done ------------------------>')
    redraw = True
    eq_hov = False
    eq_draw = eq_pic
##    options_hov = False
##    options_draw = options_pic
    volume_timer = -9001
    while True:
        if volume_timer > 0:
            volume_timer -= 1
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
                    program_loop()
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
                        print ("Default sink set to ",sink_list_index[0])
                        sink = sink_list_index[0]
                        sink_index = 0
                        if moving_inputs == True:
                            switch_sink_inputs(0,sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_2:
                    if sink_count > 1:
                        print ("Default sink set to ",sink_list_index[1])
                        sink = sink_list_index[1]
                        sink_index = 1
                        if moving_inputs == True:
                            switch_sink_inputs(1,sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_3:
                    if sink_count > 2:
                        print ("Default sink set to ",sink_list_index[2])
                        sink = sink_list_index[2]
                        sink_index = 2
                        if moving_inputs == True:
                            switch_sink_inputs(2,sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_4:
                    if sink_count > 3:
                        print ("Default sink set to ",sink_list_index[3])
                        sink = sink_list_index[3]
                        sink_index = 3
                        if moving_inputs == True:
                            switch_sink_inputs(3,sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_5:
                    if sink_count > 4:
                        print ("Default sink set to ",sink_list_index[4])
                        sink = sink_list_index[4]
                        sink_index = 4
                        if moving_inputs == True:
                            switch_sink_inputs(4,sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and volume<150:
                    higher()
                    redraw = True
                if event.button == 5 and volume>0:
                    lower()
                    redraw = True
                elif event.button == 1:
                    if check_equalizer == True:
                        if mouse_pos[0] < scx/12.5+64 and mouse_pos[0] > scx/12.5:
                            if mouse_pos[1] < scy/1.5+64 and mouse_pos[1] > scy/1.5:
                                equalizer()
                                redraw = True
                    if mouse_pos[0] < scx/3.57 and mouse_pos[0] > scx/12.5:
                            if mouse_pos[1] < scy/3 and mouse_pos[1] > scy/3.75+4:
                                reset_sinks()

        
        if mouse_pos[0] < scx/12.5+64 and mouse_pos[0] > scx/12.5:
            if mouse_pos[1] < scy/1.5+64 and mouse_pos[1] > scy/1.5:
                eq_draw = eq_pic_hov
                redraw = True
                eq_hov = True
##        if mouse_pos[0] < scx/4.16+64 and mouse_pos[0] > scx/4.16:
##            if mouse_pos[1] < scy/1.5+64 and mouse_pos[1] > scy/1.5:
##                options_draw = options_pic_hov
##                redraw = True
##                options_hov = True                

        if eq_hov == True:
            if mouse_pos[0] > scx/12.5+48 or mouse_pos[0] < scx/12.5 or mouse_pos[1] > scy/1.5+48 or mouse_pos[1] < scy/1.5:
                eq_draw = eq_pic
                redraw = True
                eq_hov = False
##        if options_hov == True:
##            if mouse_pos[0] > scx/4.16+48 or mouse_pos[0] < scx/4.16 or mouse_pos[1] > scy/1.5+48 or mouse_pos[1] < scy/1.5:
##                options_draw = options_pic
##                redraw = True
##                options_hov = False
                  
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
            
            if check_equalizer == True:
                draw_picture(scx/12.5,scy/1.5,eq_draw)
##            draw_picture(scx/4.16,scy/1.5,options_draw)
                    
            pygame.display.update()
            redraw = False
            
        clock.tick(60)

def program_loop():
    global volume_timer, reset_timer, sink, sink_list, sink_list_index, sink_count
    input_list, text_list, bar_list,bar_list2, bar_list3 = reset_inputs_list()
    bar2 = 100*1.5
    bar3 = 22
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
                            if input_list[count][2] < 100:
                                input_list[count][2] += 5
                                if input_list[count][2] > 100:
                                    input_list[count][2] = 100
                                bar[2] = input_list[count][2]*1.5
                                set_input_volume(input_list[count][0],input_list[count][2])
                        count += 1
                    if move == 1:
                        for bar in bar_list:
                            bar[1] += 10
                        for bar in bar_list2:
                            bar[1] += 10
                        for bar in bar_list3:
                            bar[1] += 10
                        for text in text_list:
                            text[3] += 10
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
                    redraw = True
                elif event.button == 1:
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

            for bar in bar_list2:
                if mouse_pos[0] < bar[0]+bar2 and mouse_pos[0] > bar[0]:
                    if mouse_pos[1] < bar[1] + bar[3] and mouse_pos[1] > bar[1]:
                        bar[5] = 1
                        redraw = True
            for bar in bar_list2:
                if bar[5] > 0:
                    if mouse_pos[0] > bar[0]+bar2 or mouse_pos[0] < bar[0] or mouse_pos[1] > bar[1] + bar[3] or mouse_pos[1] < bar[1]:
                        bar[5] = 0
                        redraw = True
            for bar in bar_list3:
                if mouse_pos[0] < bar[0]+bar3 and mouse_pos[0] > bar[0]:
                    if mouse_pos[1] < bar[1] + bar[3] and mouse_pos[1] > bar[1]:
                        bar[5] = 1
                        redraw = True
            for bar in bar_list3:
                if bar[5] > 0:
                    if mouse_pos[0] > bar[0]+bar3 or mouse_pos[0] < bar[0] or mouse_pos[1] > bar[1] + bar[3] or mouse_pos[1] < bar[1]:
                        bar[5] = 0
                        redraw = True
                        
        if redraw == True:
            Display.fill(grey)
            for bar in bar_list:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],bar[4])
            for bar in bar_list2:
                if bar[5] == 0:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],bar[4])
                else:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],blue)
            for bar in bar_list3:
                if bar[7] > -1:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],green)
                if bar[7] == -1:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],bar[4])
                if bar[5] == 1:
                    draw_bar(bar[0],bar[1],bar[2],bar[3],red)
            for text in text_list:
                draw_text(text[0],text[1],text[2],text[3],text[4],text[5],text[6])
            redraw = False
            pygame.display.update()
            
        clock.tick(60)
        
main_loop()
pygame.quit()
quit()
