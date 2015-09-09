#!/usr/bin/env python
import pygame
import sys
import os
import subprocess
import find_sinks


sink_list = find_sinks.sec()
sink = find_sinks.read_settings('default_sink = ')
print (sink_list)
print ('Default sink: ', sink)
pygame.init()
Display = pygame.display.set_mode((500,300))
pygame.display.set_caption('Volum')
icon = pygame.image.load('load/volum.png')
eq_pic = pygame.image.load('load/eqpic.png')
eq_pic_hov = pygame.image.load('load/eqpic_hov.png')
clock = pygame.time.Clock()
pygame.display.set_icon(icon)

white = (255,255,255)
grey = (235,235,235)
red = (255,100,100)
black = (0,0,0)
dark = (35,35,35)
blue = (80,80,150)
green = (0,255,0)
blgr = (54,87,99)

volume = 50

def eq_button(x,y,picture):
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
    global volume
    volume+=5
    sys_arg_volum(volume)

def lower():
    global volume
    volume-=5
    sys_arg_volum(volume)

def sys_arg_volum(volume):
    global sink
    os.system("load/./arg_pactl.sh %s %s" % (sink, volume))

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


def main_loop():
    global volume
    global sink
    global sink_list
    check_equalizer = os.path.exists('/usr/bin/qpaeq')
    check_equalizer = os.path.exists('/usr/local/bin/qpaeq')
    sink_count = len(sink_list)
    redraw = True
    eq_hov = False
    eq_draw = eq_pic
    while True:
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
                        print ("Switched to sink 0")
                        sink = 0
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_2:
                    if sink_count > 1:
                        print ("Switched to sink 1")
                        sink = 1
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_3:
                    if sink_count > 2:
                        print ("Switched to sink 2")
                        sink = 2
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_4:
                    if sink_count > 3:
                        print ("Switched to sink 3")
                        sink = 3
                        find_sinks.write_settings('default_sink',sink)
                        redraw = True
                if event.key == pygame.K_5:
                    if sink_count > 4:
                        print ("Switched to sink 4")
                        sink = 4
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
                        if mouse_pos[0] < 40+64 and mouse_pos[0] > 40:
                            if mouse_pos[1] < 200+64 and mouse_pos[1] > 200:
                                equalizer()
                                redraw = True

        
        if mouse_pos[0] < 40+64 and mouse_pos[0] > 40:
            if mouse_pos[1] < 200+64 and mouse_pos[1] > 200:
                eq_draw = eq_pic_hov
                redraw = True
                eq_hov = True

                
        if eq_hov == True:
            if mouse_pos[0] > 40+48 or mouse_pos[0] < 40 or mouse_pos[1] > 200+48 or mouse_pos[1] < 200:
                eq_draw = eq_pic
                redraw = True
                eq_hov = False
                  
        
        if redraw == True:
            Display.fill(grey)

            draw_bar(38,38,150*2.8+4,34,black)
            if volume <105:
                draw_bar(40,40,volume*2.8,30,red)
            if volume > 100:
                draw_bar(40,40,100*2.8,30,red)
                draw_bar(40+100*2.8,40,(volume-100)*2.8,30,blue)
            draw_text('',volume,45,42,22,white,1)
            draw_text('Sink: ',sink_list[int(sink)],42,82,18,black,2)
            
            if check_equalizer == True:
                eq_button(40,200,eq_draw)
                    
            pygame.display.update()
            redraw = False
            
        clock.tick(60)

main_loop()
pygame.quit()
quit()
