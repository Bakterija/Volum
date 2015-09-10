#!/usr/bin/env python
import pygame, sys, os, subprocess, find_sinks

pygame.init()
sink_list = find_sinks.sec()
sink = find_sinks.read_settings('default_sink = ')
scx = int(find_sinks.read_settings('X_window_size = '))
scy = int(find_sinks.read_settings('Y_window_size = '))
Display = pygame.display.set_mode((scx,scy))
print (sink_list)
print ('Default sink: ', sink)
pygame.display.set_caption('Volum')
icon = pygame.image.load('load/volum.png')
eq_pic = pygame.image.load('load/eqpic.png')
eq_pic_hov = pygame.image.load('load/eqpic_hov.png')
##options_pic = pygame.image.load('load/optionspic.png')
##options_pic_hov = pygame.image.load('load/optionspic_hov.png')
clock = pygame.time.Clock()
pygame.display.set_icon(icon)

white = (255,255,255)
grey = (235,235,235)
red = (255,100,100)
black = (0,0,0)
dark = (35,35,35)
blue = (80,80,150)
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

def switch_sink_inputs(new_default):
    inputs_to_move = find_sinks.change_sink()
    os.system("load/./set_default_sink.sh %s" % (new_default))
    for inputs in inputs_to_move:
        os.system("load/./switch_inputs.sh %s %s" % (inputs,new_default))
    print ('Switched: ', inputs_to_move,' to sink ', new_default)


def main_loop():
    global volume, volume_timer, reset_timer, sink, sink_list, screen_x, screen_y
    reset_timer = int(find_sinks.read_settings('timer = '))
    if reset_timer < 0:
        reset_timer = 0
    check_equalizer = os.path.exists('/usr/bin/qpaeq')
    if check_equalizer == False:
        check_equalizer = os.path.exists('/usr/local/bin/qpaeq')
    sink_count = len(sink_list)
    inputs = find_sinks.change_sink()
    print ('Inputs: ', inputs)
    redraw = True
    eq_hov = False
    eq_draw = eq_pic
##    options_hov = False
##    options_draw = options_pic
    volume_timer = -9001
    volume = 50
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
                if event.key == pygame.K_1:
                    if sink_count > 0:
                        print ("Default sink set to 0")
                        sink = 0
                        switch_sink_inputs(sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_2:
                    if sink_count > 1:
                        print ("Default sink set to 1")
                        sink = 1
                        switch_sink_inputs(sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_3:
                    if sink_count > 2:
                        print ("Default sink set to 2")
                        sink = 2
                        switch_sink_inputs(sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_4:
                    if sink_count > 3:
                        print ("Default sink set to 3")
                        sink = 3
                        switch_sink_inputs(sink)
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_5:
                    if sink_count > 4:
                        print ("Default sink set to 4")
                        sink = 4
                        switch_sink_inputs(sink)
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
            draw_text('Sink: ',sink_list[int(sink)],scx/12.5+2,scy/3.75+2,18,black,2)
            
            if check_equalizer == True:
                draw_picture(scx/12.5,scy/1.5,eq_draw)
##            draw_picture(scx/4.16,scy/1.5,options_draw)
                    
            pygame.display.update()
            redraw = False
            
        clock.tick(60)

main_loop()
pygame.quit()
quit()
