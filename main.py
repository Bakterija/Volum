#!/usr/bin/env python

import os, subprocess, sys
from app_modules.pyver import PY3
from app_modules.global_vars import *
from app_modules import file_handler
from app_modules.pa_controller import PAController
from app_modules.widgets.msg_binder import MsgBinder
try:
    from Tkinter import *
    from Tkinter import Button as tkButton
    from Tkinter import Label as tkLabel
    from ttk import Style as ttkStyle
    from ttk import Button
    from ttk import Checkbutton
    from ttk import Radiobutton
    from ttk import Combobox
    from ttk import Menubutton
    from ttk import Scale
    from ttk import Separator
    from ttk import Treeview
    from ttk import Widget
    from tkFileDialog import askopenfilename
    from tkFileDialog import askdirectory
    from tkColorChooser import askcolor
    from PIL import ImageTk
    import tkFont, tkMessageBox
    ##from ttk import Label
    ##from ttk import Frame as ttkFrame
except:
    from tkinter import *
    from tkinter import Button as tkButton
    from tkinter import Label as tkLabel
    from tkinter.ttk import Style as ttkStyle
    from tkinter.ttk import Button
    from tkinter.ttk import Checkbutton
    from tkinter.ttk import Radiobutton
    from tkinter.ttk import Combobox
    from tkinter.ttk import Menubutton
    from tkinter.ttk import Scale
    from tkinter.ttk import Separator
    from tkinter.ttk import Treeview
    from tkinter.ttk import Widget
    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import askdirectory
    from tkinter.colorchooser import askcolor
    from PIL import ImageTk as ImageTk
    import tkinter.font as tkFont
    import tkinter.messagebox as tkMessageBox
from threading import Thread
from random import randrange
from PIL import Image as Pillow_image
import time

def return_picture(path):
    img = Pillow_image.open(path)
    img = ImageTk.PhotoImage(img)
    return img

def set_winicon(window, path):
    try:
        img = Pillow_image.open(path)
        img = ImageTk.PhotoImage(img)
        window.tk.call('wm', 'iconphoto', window._w, img)
        # window.iconbitmap('path')
    except:
        print ("Couldn not load Linux icon")

def open_equalizer(*args):
    if EQUALIZER == 'pulse-eq-gtk':
        os.system("pulseaudio-equalizer-gtk")
    elif EQUALIZER == 'qpaeq':
        os.system("qpaeq")

def set_input_volume(index,volume):
    volume = volume * 655
    subprocess.Popen('pacmd set-sink-input-volume %s %s' % (index, volume),
                     shell=True,stdout=subprocess.PIPE)
    gui_handler.reset_timer()

def set_sink_volume(index,volume):
    volume = volume * 655
    subprocess.Popen('pacmd set-sink-volume %s %s' % (index, volume),
                     shell=True,stdout=subprocess.PIPE)
    gui_handler.reset_timer()

def switch_input_sink(sinput,new_sink):
    subprocess.Popen('pacmd move-sink-input %s %s' % (sinput[0], new_sink),
                     shell=True,stdout=subprocess.PIPE)
    time.sleep(0.05)
    set_input_volume(sinput[0], sinput[2])
    gui_handler.reset_timer()

def move_inputs_to_sink(index):
    inputs_to_move = pac.return_inputs()
    subprocess.Popen("pacmd set-default-sink %s" % (index[0]),
                     shell=True,stdout=subprocess.PIPE)
    for inputs in inputs_to_move:
        switch_input_sink(inputs,index[0])
    for x in inputs_to_move:
        print ('Switched: ', x[0],' '+x[4]+' ',' to ', index[2])
    gui_handler.reset_timer()

def get_dict_item(dictio, item, default):
    for k, v in dictio.items():
        if k == item:
            return v
    return default


class App_handler:
    def __init__(self, parent, **kwargs):
        bg = get_dict_item(kwargs,'bg','red')
        self.frame_list = []
        self.app_placement = 0
        self.app_place_interval = 30
        self.parent = parent
        self.create_frame(bg)

    def create_frame(self, bg):
        self.frame = Frame(self.parent, width=X_root, height=Y_root,bg=bg)
        self.frame.pack_propagate(0)
        self.frame.pack()

        self.parent.bind('<Button-5>', self.frame_place_UP)
        self.parent.bind('<Button-4>', self.frame_place_DOWN)
        self.frame.bind('<Button-5>', self.frame_place_UP)
        self.frame.bind('<Button-4>', self.frame_place_DOWN)

    def add(self, parent, index, **kwargs):
        media_name = get_dict_item(kwargs,'media_name','n/a')
        volume = int(get_dict_item(kwargs,'volume', 50))
        sink = int(get_dict_item(kwargs,'sink', 0))
        app_name = get_dict_item(kwargs,'app_name', 'n/a')
        if app_name == 'n/a':
            app_name = media_name
        y_adjustment = 0 + self.app_placement +(
            self.app_place_interval* len(self.frame_list))
        App_frame(self.frame, index, y_adjustment, media_name, volume, sink, app_name)
        self.frame_list[-1].frame.bind('<Button-5>', self.frame_place_UP)
        self.frame_list[-1].frame.bind('<Button-4>', self.frame_place_DOWN)
        self.frame_list[-1].name.bind('<Button-5>', self.frame_place_UP)
        self.frame_list[-1].name.bind('<Button-4>', self.frame_place_DOWN)

    def reset_listlen(self,input_list):
        current_len = len(self.frame_list)
        new_len = len(input_list)
        return current_len, new_len
    def update(self,input_list):
        current_len, new_len = self.reset_listlen(input_list)
        while current_len > new_len:
            self.frame_list[-1].destroy()
            self.frame_list.pop(-1)
            current_len, new_len = self.reset_listlen(input_list)
        while current_len < new_len:
            self.add(gui_handler.frame1, 0)
            current_len, new_len = self.reset_listlen(input_list)
        cnt = 0
        for index, media_name, volume, sink, app_name in input_list:
            self.frame_list[cnt].configure(
                index=index, media_name=media_name, volume=volume,
                sink=sink, app_name=app_name)
            cnt += 1

    def placement_task(self, *arg):
        adj = 0
        for x in self.frame_list:
            if self.app_placement+adj < 0:
                x.frame.place_configure(y=6200)
            else:
                x.frame.place_configure(y=adj+self.app_placement)
            adj+= self.app_place_interval

    def frame_place_UP(self, *arg):
        self.app_placement -= self.app_place_interval/2
        self.frame.after(2, self.placement_task)

    def frame_place_DOWN(self, *arg):
        self.app_placement += self.app_place_interval/2
        self.frame.after(2, self.placement_task)


class App_frame:
    def __init__(self, parent, index, y_adjustment, media_name,
                 volume, sink, app_name):
        global app_handler
        self.parent = parent
        self.index = index
        self.y_adj = y_adjustment
        self.media_name = media_name
        self.volume = volume
        self.sink = sink
        self.app_name = app_name
        self.button_list = []
        self.volcol = (vol_red,vol_blue)

        self.frame = Frame(
            parent, width=int(X_root)-60, height=20,bg=gui_handler.bg_color)
        self.frame.pack_propagate(0)
        self.frame.place(x=30, y=self.y_adj)
        self.frame_btn = Frame(self.frame, height=20,bg=gui_handler.bg_color)
        self.frame_btn.pack(side=RIGHT)
        ## appends to app_handlers list
        app_handler.frame_list.append(self)

        self.name = Label(
            self.frame, text=self.app_name, font=('Droid sans',12,'normal'),
            background=gui_handler.bg_color)
        self.name.pack(side=LEFT)

        self.add_sink_buttons()

        self.canva = Canvas(
            self.frame, width=180, height=20, bg='black', bd=0,
            highlightthickness=0, relief= SUNKEN)
        self.canva.pack(side=RIGHT,padx=10)
        self.redraw_volume()

        self.canva.bind('<Enter>', self.on_enter)
        self.canva.bind('<Leave>', self.on_leave)
        self.canva.bind('<Button-4>', self.volume_UP)
        self.canva.bind('<Button-5>', self.volume_DOWN)

    def add_sink_buttons(self):
        eval_command = lambda x,x2: (lambda : self.switch_sink(x,x2))
        for x in gui_handler.sinks:
            bgcol = lblue
            if int(self.sink) == int(x[0]):
                bgcol = vol_green
            btn = MsgBinder(
                self.frame_btn, text=x[2][:2], bg=bgcol,width=28,
                bg_hov=vol_red, font=('Droid sans',11,'normal'),
                func='func', command=eval_command(
                    (self.index, self.app_name, self.volume), x[0]))
            btn.pack(side=RIGHT,padx=2)
            self.button_list.append(btn)
    def reset_sink_buttons(self):
        for x in self.button_list:
            x.destroy()
        self.add_sink_buttons()

    def redraw_volume(self):
        self.canva.delete(ALL)
        volume = float(self.volume)
        if self.volume <= 100:
            self.canva.create_rectangle(
                1, 1, volume/100*150, 19, fill=self.volcol[0], outline='')
        else:
            self.canva.create_rectangle(
                1, 1, volume/100*150, 19, fill=self.volcol[0], outline='')
            self.canva.create_rectangle(
                150, 1, volume/100*150, 19, fill=self.volcol[1], outline='')
        self.canva.create_text(
            (0,10),anchor=W, text=' %s' % (self.volume),
            font= ('Liberation sans', 11, 'bold'), fill='white')

    def on_enter(self,*arg):
        self.volcol = (vol_red2,vol_blue2)
        self.redraw_volume()

    def on_leave(self,*arg):
        self.volcol = (vol_red,vol_blue)
        self.redraw_volume()

    def volume_UP(self,*arg):
        if self.volume < 120:
            self.volume += 5
            self.redraw_volume()
            gui_handler.timer2 = 160
            gui_handler.reset_timer()
            gui_handler.timed_event = lambda: set_input_volume(
                self.index, self.volume)
    def volume_DOWN(self,*arg):
        if self.volume > 0:
            self.volume -= 5
            self.redraw_volume()
            gui_handler.timer2 = 160
            gui_handler.reset_timer()
            gui_handler.timed_event = lambda: set_input_volume(
                self.index, self.volume)

    def switch_sink(self,sinput,new_index):
        switch_input_sink(sinput,new_index)
        self.sink = new_index
        self.reset_sink_buttons()

    def configure(self,**kwargs):
        self.media_name = get_dict_item(kwargs,'media_name','n/a')
        self.volume = int(get_dict_item(kwargs,'volume', 50))
        self.sink = int(get_dict_item(kwargs,'sink', 0))
        self.app_name = get_dict_item(kwargs,'app_name', 'n/a')
        if self.app_name == 'n/a': self.app_name = self.media_name
        if len(self.app_name) > 14: self.app_name = self.app_name[:12]+'..'
        self.index = int(get_dict_item(kwargs,'index', 0))
        self.name.configure(text=self.app_name)
        self.redraw_volume()
        self.reset_sink_buttons()

    def destroy(self,*arg):
        self.frame.destroy()



class GUI_handler:
    def __init__(self):
        global pac
        self.eq_picture = return_picture('load/eqpic.png')
        self.eq_picture_hov = return_picture('load/eqpic_hov.png')
        self.bg_color = window_bgcol
        self.label_color = '#E1E1E1'
        self.volcol = (vol_red,vol_blue)
        self.muted_volcol = (blgr,blgr2)
        self.timer = 1500
        self.timer2 = -99
        self.timed_event = None
        self.sinks = pac.return_sinks()
        self.sink_index = int(default_sink)
        try:
            self.active_sink = self.sinks[self.sink_index]
        except:
            print ('Sink not found, switching to 0')
            try:
                self.active_sink = self.sinks[0]
                self.sink_index = 1
            except:
                print ('No sink found')
        self.volume = self.active_sink[1]
        self.inputs = pac.return_inputs()
        self.muted = False
        self.back_frame = Frame(
            root, width=X_root, height=Y_root, bg=self.bg_color)
        self.back_frame.pack_propagate(0)
        self.back_frame.pack()


        self.frame2 = Frame(
            self.back_frame, width=X_root, height=20,bg=self.bg_color)
        self.frame2.pack_propagate(0)
        self.frame2.pack(padx=30, pady=10)

        # Device:: / App:: buttons
        self.device_btn = MsgBinder(
            self.frame2, text="Device::", font=('Droid sans',11,'normal'),
            width='+70', fg='black', bg_hov='#B4B4F5', bg=self.bg_color,
            func='func', command=self.device_tab)
        self.device_btn.pack(side=LEFT)
        self.app_btn = MsgBinder(
            self.frame2,text="Applications::",font=('Droid sans',11,'normal'),
            width='+120', fg='black', bg_hov='#B4B4F5', bg=self.bg_color,
            func='func', command=self.app_tab)
        self.app_btn.pack(side=LEFT,padx=10)

        root.config(bg=self.bg_color)
        self.frame1 = Frame(root)
        self.device_tab()

        root.bind('<F1>', lambda x: self.device_tab())
        root.bind('<F2>', lambda x: self.app_tab())
        root.bind('<e>', self.toggle_input_moving)
        root.after(100, self.timer_task)
        root.after(20, self.timer2_task)

    def reset_frame1(self):
        self.frame1.destroy()
        self.frame1 = Frame(
            self.back_frame, width=X_root, height=Y_root,bg=self.bg_color)
        self.frame1.pack_propagate(0)
        self.frame1.pack()
        self.timer = 0

    def device_tab(self):
        self.active_tab = 'device'
        self.device_btn.configure(bg=self.label_color)
        self.app_btn.configure(bg=self.bg_color)
        self.reset_frame1()
        self.volume_canva = Canvas(
            self.frame1, width=150.0*500.0/178.571, height=300/10+4,
            bg='black', bd=0, highlightthickness=0, relief=SUNKEN)
        self.volume_canva.pack(anchor=NW,padx=30,pady=10)
        self.redraw_volume_bar()

        self.eq_button = MsgBinder(
            self.frame1, img=self.eq_picture, img_hov=self.eq_picture_hov,
            bg=self.bg_color, width=60,func='func',
            command=lambda : open_equalizer())
        self.eq_button.pack(side=BOTTOM,padx=30,pady=30)

        if m_inputs == 1:
            bgcol = 'black'
        else:
            bgcol = vol_red2
        self.sink_label = Label(
            self.frame1, text='Sink: %s' % (self.active_sink[2]),
            font=('Droid sans',14,'normal'), foreground=bgcol,
            background=self.bg_color)
        self.sink_label.pack(anchor=NW,padx=30)

        for x in (self.volume_canva, self.sink_label, self.frame1):
            x.bind('<Button-4>', self.volume_UP)
            x.bind('<Button-5>', self.volume_DOWN)
        root.bind('<Right>', self.volume_UP)
        root.bind('<Left>', self.volume_DOWN)
        root.bind('<Up>', self.volume_UP)
        root.bind('<Down>', self.volume_DOWN)
        root.bind('<d>', self.volume_UP)
        root.bind('<a>', self.volume_DOWN)
        root.bind('<KP_Add>', self.volume_UP)
        root.bind('<KP_Subtract>', self.volume_DOWN)
        root.bind('<Escape>', lambda x: {root.quit(), root.destroy()})
        root.bind('<q>', open_equalizer)
        root.bind('<m>', self.toggle_mute)

        eval_command = lambda x: (lambda p: self.switch_active_sink(x))
        for i, x in enumerate(self.sinks):
            root.bind(str(i+1), eval_command(x[0]))
        self.volume_canva.bind('<Enter>', self.on_vol_enter)
        self.volume_canva.bind('<Leave>', self.on_vol_leave)
        for x in self.frame2, self.sink_label, self.frame1, self.volume_canva:
            x.bind('<Button-3>', self.toggle_mute)

    def app_tab(self):
        global app_handler
        self.device_btn.configure(bg=self.bg_color)
        self.app_btn.configure(bg=self.label_color)
        self.active_tab = 'app'
        self.reset_frame1()
        self.app_list = []
        app_handler = App_handler(self.frame1, bg=self.bg_color)
        app_handler.update(self.inputs)


    def toggle_input_moving(self,*arg):
        global m_inputs
        if m_inputs == 0:
            m_inputs = 1
            self.sink_label.configure(foreground='black')
        else:
            m_inputs = 0
            self.sink_label.configure(foreground=vol_red2)
        file_handler.write_settings('m_inputs', m_inputs)

    def on_vol_enter(self,*arg):
        self.volcol = (vol_red2,vol_blue2)
        self.redraw_volume_bar()

    def on_vol_leave(self,*arg):
        self.volcol = (vol_red,vol_blue)
        self.redraw_volume_bar()

    def switch_active_sink(self,new_index):
        for i, x in enumerate(self.sinks):
            if x[0] == new_index: break
        self.sink_label.config(text='Sink: '+self.sinks[i][2])
        self.sink_index = i
        self.active_sink = self.sinks[i]
        file_handler.write_settings('default_sink',self.sink_index)
        self.volume = self.active_sink[1]
        self.redraw_volume_bar()
        if m_inputs == 1:
            move_inputs_to_sink(self.active_sink)

    def volume_UP(self,*arg):
        gui_handler.reset_timer()
        if self.muted == True:
            self.toggle_mute()
        if self.volume < 150:
            self.volume += 2
            if self.active_tab == 'device':
                self.redraw_volume_bar()
            self.timer2 = 200
            self.timed_event = lambda: set_sink_volume(
                self.active_sink[0], self.volume)
            root.title('Vol. - %s' % (self.volume))

    def volume_DOWN(self,*arg):
        gui_handler.reset_timer()
        if self.muted == True:
            self.toggle_mute()
        if self.volume > 0:
            self.volume -= 2
            if self.active_tab == 'device':
                self.redraw_volume_bar()
            self.timer2 = 200
            self.timed_event = lambda: set_sink_volume(
                self.active_sink[0],self.volume)
            root.title('Vol. - %s' % (self.volume))

    def redraw_volume_bar(self):
        if self.muted == True:
            volume = self.muted_volume
            volcol = self.muted_volcol
        else:
            volume = self.volume
            volcol = self.volcol
        self.volume_canva.delete(ALL)
        if volume <= 100:
            self.volume_canva.create_rectangle(
                2, 2, volume*500/178.571, 300/10+2, fill=volcol[0], outline='')
        else:
            self.volume_canva.create_rectangle(
                2, 2, 100*500/178.571, 300/10+2, fill=volcol[0], outline='')
            self.volume_canva.create_rectangle(
                100*500/178.571, 2, volume*500/178.571-2,
                300/10+2, fill=volcol[1], outline='')
        self.volume_canva.create_text(
            (0,(300/10+4)/2),anchor=W, text=' '+str(volume),
            font= ('Liberation sans', 16, 'bold'), fill='white')

    def refresh(self):
        '''Refreshes Pulse Audio information'''
        pac.reset_sinks_inputs()
        if pac.reload_gui == True:
            pac.reload_gui = False
            self.sinks = pac.return_sinks()
            self.inputs = pac.return_inputs()
            self.active_sink = self.sinks[self.sink_index]
            if self.active_tab == 'device':
                self.volume = self.active_sink[1]
                self.redraw_volume_bar()
            elif self.active_tab == 'app':
                app_handler.update(self.inputs)
            root.title('Vol. - '+str(self.volume))

    def timer_task(self):
        '''Runs a function, usually volume change,
        a set amount of time after last input'''
        self.timer -= 100
        if self.timer < 0:
            self.reset_timer()
            self.refresh()
        root.after(100, self.timer_task)

    def timer2_task(self):
        if self.timer2 > 0:
            self.timer2 -= 20
            if self.timer2 == 0:
                self.timed_event()
                self.timer2 = -99
        root.after(20, self.timer2_task)

    def reset_timer(self):
        self.timer = 1000

    def toggle_mute(self, *arg):
        if self.muted == False:
            self.muted = True
            self.muted_volume, self.volume = self.volume, 0
            self.timer2 = 40
            self.timed_event = lambda: set_sink_volume(self.active_sink[0],0)
            gui_handler.reset_timer()
            self.redraw_volume_bar()
            self.bg_color = window_bgcol2
            for x in (self.eq_button, self.frame2, self.sink_label,
                      self.frame1, self.back_frame):
                x.configure(bg=self.bg_color)
            root.title("Muted")
        else:
            self.muted = False
            self.volume = self.muted_volume
            self.timer2 = 40
            self.timed_event = lambda: set_sink_volume(
                self.active_sink[0],self.volume)
            gui_handler.reset_timer()
            self.redraw_volume_bar()
            self.bg_color = window_bgcol
            for x in (self.eq_button, self.frame2, self.sink_label,
                      self.frame1, self.back_frame):
                x.configure(bg=self.bg_color)
            root.title('sPAGUI %s' % (__VERSION__))

if __name__ == '__main__':
    ## Load settings
    default_sink = int(file_handler.read_settings('default_sink=','0'))
    X_root = file_handler.read_settings('X_root=','500')
    Y_root = file_handler.read_settings('Y_root=','300')
    m_inputs = int(file_handler.read_settings('m_inputs=',1))
    ## Global vars
    __VERSION__ = 2

    root = Tk()
    root.title('sPAGUI %s' % (__VERSION__))
    root.minsize(500,300)
    root.geometry('%sx%s' % (X_root,Y_root))
    maxsize = "5x5"

    def startup_task():
        global gui_handler, pac
        set_winicon(root,'load/icon.ico')
        pac = PAController()
        gui_handler = GUI_handler()

    ##root.protocol('WM_DELETE_WINDOW', closewin)
    root.after(0, startup_task)
    root.mainloop()
