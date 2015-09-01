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
gameDisplay = pygame.display.set_mode((500,300))
pygame.display.set_caption('Volum')
ikona = pygame.image.load('load/volum.png')
eq_bilde = pygame.image.load('load/eqpic.png')
eq_bilde_hov = pygame.image.load('load/eqpic_hov.png')
clock = pygame.time.Clock()
pygame.display.set_icon(ikona)

white = (255,255,255)
grey = (235,235,235)
red = (255,100,100)
black = (0,0,0)
dark = (35,35,35)
blue = (80,80,150)
green = (0,255,0)

volum = 50

def eq_poga(x,y,bilde):
    gameDisplay.blit(bilde,(x,y))
    
def draw_text(text,variable,x,y,size,color,font):
    if font == 1:
        font_path = os.getcwd()+('/load/font.ttf')
    if font == 2:
        font_path = os.getcwd()+('/load/font2.ttf')
    font = pygame.font.Font(font_path,size)
    text = font.render((text + str(variable)), True, color)
    gameDisplay.blit(text, (x,y))

def draw_bar(bars_x, bars_y, bars_w, bars_h, color):  
    pygame.draw.rect(gameDisplay, color, [bars_x, bars_y, bars_w, bars_h])

def skalak():
    global volum
    if volum < 150:
        volum+=5
    sys_arg_volum(volum)

def klusak():
    global volum
    if volum > 0:
        volum-=5
    sys_arg_volum(volum)

def sys_arg_volum(volum):
    global sink
    os.system("load/./arg_pactl.sh %s %s" % (sink, volum))

def equalizer():
    os.system("load/./equalizer.sh")

def get_volums():
    komanda = subprocess.Popen(["amixer"], stdout=subprocess.PIPE)
    output = komanda.communicate()[0]
    output2 = output.decode('utf-8')
    output3 = output2.find('%')
    output4 = output2[output3-3:output3]
    output5 = output4.replace('[','')
    return int(output5)


def main_loop():
    global volum
    global sink
    global sink_list
    sink_count = len(sink_list)
    redraw = True
    eq_hov = False
    bilde = eq_bilde
    while True:
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d and volum<150:
                    skalak()
                    redraw = True
                if event.key == pygame.K_a and volum>0:
                    klusak()
                    redraw = True
                if event.key == pygame.K_RIGHT and volum<150:
                    skalak()
                    redraw = True     
                if event.key == pygame.K_LEFT and volum>0:
                    klusak()
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
                if event.button == 4 and volum<150:
                    skalak()
                    redraw = True
                if event.button == 5 and volum>0:
                    klusak()
                    redraw = True
                elif event.button == 1:
                    if mouse_pos[0] < 40+64 and mouse_pos[0] > 40:
                        if mouse_pos[1] < 200+64 and mouse_pos[1] > 200:
                            equalizer()
                            redraw = True

        
        if mouse_pos[0] < 40+64 and mouse_pos[0] > 40:
            if mouse_pos[1] < 200+64 and mouse_pos[1] > 200:
                bilde = eq_bilde_hov
                redraw = True
                eq_hov = True

                
        if eq_hov == True:
            if mouse_pos[0] > 40+48 or mouse_pos[0] < 40 or mouse_pos[1] > 200+48 or mouse_pos[1] < 200:
                bilde = eq_bilde
                redraw = True
                eq_hov = False
                  
        
        if redraw == True:
            gameDisplay.fill(grey)

            draw_bar(38,38,150*2.8+4,34,black)
            if volum <105:
                draw_bar(40,40,volum*2.8,30,red)
            if volum > 100:
                draw_bar(40,40,100*2.8,30,red)
                draw_bar(40+100*2.8,40,(volum-100)*2.8,30,blue)
            draw_text('',volum,45,42,22,white,1)
            draw_text('Sink: ',sink_list[int(sink)],42,82,18,black,2)

            eq_poga(40,200,bilde)
                
            pygame.display.update()
            redraw = False
            
        clock.tick(60)

main_loop()
pygame.quit()
quit()
