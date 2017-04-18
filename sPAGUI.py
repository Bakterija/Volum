PY3 = False
import os, subprocess, sys
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
    PY3 = True
from threading import Thread
from random import randrange
from PIL import Image as Pillow_image
import time


def readf(filename):
    file = filename
    try:
        f = open(file, 'rU')
    except:
        savef('',filename)
        f = open(file, 'rU')
    a = f.read()
    a = str.splitlines(a)
    f.close()
    return a

def savef(text,file):
    f = open(file, 'w')
    f.write(text)
    f.close()

def edit_settings(text,text_find,new_value):
    count = 0
    newlist = []
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = text_find + '=' + str(new_value)
            newlist.append(c)
        else:
            newlist.append(lines)
        count+=1
    count = 1
    return newlist

def read_settings(*arg):
    global sys_path
    a = readf('load/settings.ini')
    a = get_settings(a,arg[0],arg[1])
    return a

def get_settings(text,text_find,default_value):
    for lines in text:
        b = lines.find(text_find)
        if b is not -1:
            c = lines[len(text_find):]
    ## Checks if it exists and appends something, if not
    try:
        if c == '':
            c = default_value
            if default_value != '':
                write_settings(text_find[:-1],'\n'+c)
    except:
        c = default_value
        fh = open('load/settings.ini', 'a')
        fh.write('\n'+str(text_find)+str(c))
        fh.close()
    return c

def write_settings(text_find,new_value):
    global sys_path
    a = readf('load/settings.ini')
    a = edit_settings(a,text_find,new_value)
    text = a = '\n'.join(str(e) for e in a)
    savef(text,'load/settings.ini')

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
        print ("Couldn't load Linux icon")

def subprocess_return(INPUT):
        cmd_FORMAT = INPUT.split()
        output = subprocess.Popen(cmd_FORMAT, stdout=subprocess.PIPE).communicate()[0]
        if PY3:
            output = output.decode('utf-8')
        else:
            output = str(output)
        return output

def equalizer(equalizer_c):
    if equalizer_c == 'pulse-eq-gtk':
        os.system("pulseaudio-equalizer-gtk")
    elif equalizer_c == 'qpaeq':
        os.system("qpaeq")

def set_input_volume(index,volume):
    volume = volume*655
    subprocess.Popen('pacmd set-sink-input-volume %s %s' % (index, volume), shell=True,stdout=subprocess.PIPE)
    print (index,volume)
    gui_handler.reset_timer()

def set_sink_volume(index,volume):
    volume = volume*655
    subprocess.Popen('pacmd set-sink-volume %s %s' % (index, volume), shell=True,stdout=subprocess.PIPE)
    print (index,volume)
    gui_handler.reset_timer()

def switch_input_sink(sinput,new_sink):
    subprocess.Popen('pacmd move-sink-input %s %s' % (sinput[0], new_sink), shell=True,stdout=subprocess.PIPE)
    time.sleep(0.05)
    set_input_volume(sinput[0], sinput[2])
    gui_handler.reset_timer()

def move_inputs_to_sink(index):
    inputs_to_move = pac.return_inputs()
    subprocess.Popen("pacmd set-default-sink %s" % (index[0]), shell=True,stdout=subprocess.PIPE)
    for inputs in inputs_to_move:
        switch_input_sink(inputs,index[0])
    for x in inputs_to_move:
        print ('Switched: ', x[0],' '+x[4]+' ',' to ', index[2])
    gui_handler.reset_timer()

class PA_controller:
    def __init__(self):
        print ('-'*21+'PA_controller __init__'+'-'*21+'\n'+'-'*64)
        self.reload_gui = False
        self.startup = True
        self.sink_inputs2, self.sinks2 = [], []
        self.reset_sinks_inputs()
        self.reset_sinks_inputs()

    def return_sinks(self):
        return self.sinks

    def return_inputs(self):
        return self.sink_inputs

    def reset_sinks_inputs(self):
        if self.reload_gui == False:
            if self.startup == False:
                self.sink_inputs2, self.sinks2 = self.sink_inputs, self.sinks
            self.sink_inputs = subprocess_return('pacmd list-sink-inputs')
            self.sink_inputs = self.sink_inputs.split('\n')
            self.sink_inputs = self.get_sink_inputs(self.sink_inputs)
            if self.startup == True:
                print ('[index]  [media.name]  [volume]  [sink]  [application.name]')
                for x in self.sink_inputs:
                    print ('[%s - %s - %s - %s - %s]' % (x[0], x[1], x[2], x[3], x[4]))
                print ('-'*64+'\n'+'-'*64)
            self.sinks = subprocess_return('pacmd list-sinks')
            self.sinks = self.sinks.splitlines()
            self.sinks = self.get_sinks(self.sinks)
            if self.startup == True:
                print ('[index]  [volume] [alsa.name]  [application.name]')
                for x in self.sinks:
                    print ('[%s - %s - %s - %s]' % (x[0], x[1], x[2], x[3]))
                print ('-'*64+'\n'+'-'*64)
            if self.sink_inputs != self.sink_inputs2 or self.sinks != self.sinks2:
                self.reload_gui = True
            if self.startup == True:
                self.startup = False

    def get_sinks(self,a):
        li_count = 0
        index = -1
        newlist = []
        ## 0index, 1volume, 2name
        newlist2 = []
        for lines in a:
            b = lines.find('index:')
            if b is not -1:
                newlist.append([lines[b+7:]])
                newlist2.append([lines[b+7:]])
        for lines in a:
            b = lines.find('index:')
            if index > -1:
                newlist[index].append(lines)
            if b is not -1:
                index += 1
        index = 0
        for indexes in newlist:
            for text in indexes:
                b = text.find('alsa.name')
                if b is not -1:
                    newlist2[index].append(text[b+13:-1])
                b = text.find('volume:')
                if b is not -1:
                    c = text.find('base volume:')
                    if c is -1:
                        b = text.find('%')
                        newlist2[index].append(int(text[b-3:b]))
            index+=1
        count = 0
        for x in newlist2:
            if len(x) < 3:
                newlist2[count].append('Noname')
            count+= 1
        count = 0
        for x in newlist2:
            x.append(count)
            count+= 1
        return newlist2

    def get_sink_inputs(self,a):
        li_count = 0
        index = -1
        app_index = []
        app_name = []
        app_volume = []
        app_sink_index = []
        newlist = []
        newlist2 = []
        templist = []
        for lines in a:
            b = lines.find('index:')
            if b is not -1:
                newlist.append([lines[b+7:]])
                newlist2.append([lines[b+7:]])
        for lines in a:
            b = lines.find('index:')
            if index > -1:
                newlist[index].append(lines)
            if b != -1:
                index += 1
        index = 0
        for indexes in newlist:
            media_name,app_volume,app_sink,app_name = 'n/a','n/a','n/a','n/a'
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

def get_dict_item(dictio,item,default):
    for k, v in dictio.items():
        if k == item:
            return v
    return default

class msg_binder:
    def __init__(self,frame,**kwargs):
        text = get_dict_item(kwargs,'text','None')
        font = get_dict_item(kwargs,'font','Arial')
        width = get_dict_item(kwargs,'width','+10')
        height = get_dict_item(kwargs,'height','+5')
        self.fg = get_dict_item(kwargs,'fg','black')
        self.fg_hov = get_dict_item(kwargs,'fg_hov','')
        self.bg = get_dict_item(kwargs,'bg','')
        self.bg_hov = get_dict_item(kwargs,'bg_hov','')
        self.function = get_dict_item(kwargs,'func','False')
        self.function_exc = get_dict_item(kwargs,'command','False')
        self.img = get_dict_item(kwargs,'img','')
        self.img_hov = get_dict_item(kwargs,'img_hov','')

        if self.img == '':
            self.msg = Message(frame, text=text)
            self.msg.config(bg=self.bg, fg=self.fg, width=width, font=font)
        else:
            self.msg = Label(frame, image=self.img, width=width, background=self.bg)

        self.msg.bind("<Enter>", self._enter)
        self.msg.bind("<Leave>", self._leave)
        self.msg.bind("<Button-1>", self._click)

    def destroy(self):
        self.msg.destroy()

    def bind(self,func):
        self.msg.bind(func)

    def pack(self,**kwargs):
        side = get_dict_item(kwargs,'side','top')
        anchor = get_dict_item(kwargs,'anchor','nw')
        padx = get_dict_item(kwargs,'padx','0')
        pady = get_dict_item(kwargs,'pady','0')
        self.msg.pack(side=side, anchor=anchor, padx=padx, pady=pady)

    def _enter(self, event):
        self.msg.config(cursor="hand2")
        if self.fg_hov != '':
            self.msg.config(fg=self.fg_hov)
        if self.bg_hov != '':
            self.msg.config(bg=self.bg_hov)
        if self.img_hov != '':
            self.msg.config(image= self.img_hov)

    def _leave(self, event):
        self.msg.config(cursor="")
        if self.fg_hov != '':
            self.msg.config(fg=self.fg)
        if self.bg_hov != '':
            self.msg.config(bg=self.bg)
        if self.img_hov != '':
            self.msg.config(image= self.img)

    def _click(self, event):
        if self.function == 'func':
            self.function_exc()
        elif self.function == 'link' and self.function_exc != 'none':
            open_address_in_webbrowser(self.function_exc)

    def configure(self,**kwargs):
        self.bg = get_dict_item(kwargs,'bg','')
        self.msg.config(bg=self.bg)


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
        y_adjustment = 0 + self.app_placement +(self.app_place_interval* len(self.frame_list))
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
            self.frame_list[cnt].configure(index=index, media_name=media_name, volume=volume, sink=sink, app_name=app_name)
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
    def __init__(self, parent, index, y_adjustment, media_name, volume, sink, app_name):
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

        self.frame = Frame(parent, width=int(X_root)-60, height=20,bg=gui_handler.bg_color)
        self.frame.pack_propagate(0)
        self.frame.place(x=30, y=self.y_adj)
        self.frame_btn = Frame(self.frame, height=20,bg=gui_handler.bg_color)
        self.frame_btn.pack(side=RIGHT)
        ## appends to app_handlers list
        app_handler.frame_list.append(self)

        self.name = Label(self.frame, text=self.app_name, font=('Droid sans',12,'normal'), background=gui_handler.bg_color)
        self.name.pack(side=LEFT)

        self.add_sink_buttons()

        self.canva = Canvas(self.frame, width=180, height=20,
                                   bg='black', bd=0, highlightthickness=0, relief= SUNKEN)
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
            btn = msg_binder(self.frame_btn, text=x[2][:2], bg=bgcol,width=28, bg_hov=vol_red, font=('Droid sans',11,'normal')
                             ,func='func', command= eval_command((self.index,self.app_name,self.volume),x[0]))
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
            self.canva.create_rectangle(1, 1, volume/100*150, 19, fill=self.volcol[0], outline='')
        else:
            self.canva.create_rectangle(1, 1, volume/100*150, 19, fill=self.volcol[0], outline='')
            self.canva.create_rectangle(150, 1, volume/100*150, 19, fill=self.volcol[1], outline='')
        self.canva.create_text((0,10),anchor=W, text=' '+str(self.volume),
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
            gui_handler.timed_event = lambda: set_input_volume(self.index,self.volume)
    def volume_DOWN(self,*arg):
        if self.volume > 0:
            self.volume -= 5
            self.redraw_volume()
            gui_handler.timer2 = 160
            gui_handler.reset_timer()
            gui_handler.timed_event = lambda: set_input_volume(self.index,self.volume)

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
        self.back_frame = Frame(root, width=X_root, height=Y_root,bg=self.bg_color)
        self.back_frame.pack_propagate(0)
        self.back_frame.pack()


        self.frame2 = Frame(self.back_frame, width=X_root, height=20,bg=self.bg_color)
        self.frame2.pack_propagate(0)
        self.frame2.pack(padx=30, pady=10)

        # Device:: / App:: buttons
        self.device_btn = msg_binder(self.frame2, text="Device::", font=('Droid sans',11,'normal'), width='+70',
                        fg='black', bg_hov='#B4B4F5', bg=self.bg_color, func='func', command=self.device_tab)
        self.device_btn.pack(side=LEFT)
        self.app_btn = msg_binder(self.frame2,text="Applications::",font=('Droid sans',11,'normal'),width='+120',
                        fg='black', bg_hov='#B4B4F5', bg=self.bg_color, func='func', command=self.app_tab)
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
        self.frame1 = Frame(self.back_frame, width=X_root, height=Y_root,bg=self.bg_color)
        self.frame1.pack_propagate(0)
        self.frame1.pack()
        self.timer = 0

    def device_tab(self):
        self.active_tab = 'device'
        self.device_btn.configure(bg=self.label_color)
        self.app_btn.configure(bg=self.bg_color)
        self.reset_frame1()
        self.volume_canva = Canvas(self.frame1, width=150*500/178.571, height=300/10+4,
                                   bg='black', bd=0, highlightthickness=0, relief= SUNKEN)
        self.volume_canva.pack(anchor=NW,padx=30,pady=10)
        self.redraw_volume_bar()

        self.eq_button = msg_binder(self.frame1, img=self.eq_picture, img_hov=self.eq_picture_hov, bg=self.bg_color,
                                    width=60,func='func', command=lambda : equalizer(check_equalizer))
        self.eq_button.pack(side=BOTTOM,padx=30,pady=30)

        if m_inputs == 1:
            bgcol = 'black'
        else:
            bgcol = vol_red2
        self.sink_label = Label(self.frame1, text='Sink: '+self.active_sink[2], font=('Droid sans',14,'normal'),
                                foreground=bgcol, background=self.bg_color)
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
        write_settings('m_inputs', m_inputs)

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
        write_settings('default_sink',self.sink_index)
        self.volume = self.active_sink[1]
        self.redraw_volume_bar()
        if m_inputs == 1:
            move_inputs_to_sink(self.active_sink)

    def volume_UP(self,*arg):
        gui_handler.reset_timer()
        if self.muted == True:
            self.toggle_mute()
        if self.volume < 150:
            self.volume += 5
            if self.active_tab == 'device':
                self.redraw_volume_bar()
            self.timer2 = 200
            self.timed_event = lambda: set_sink_volume(self.active_sink[0],self.volume)
            root.title('Vol. - '+str(self.volume))
    def volume_DOWN(self,*arg):
        gui_handler.reset_timer()
        if self.muted == True:
            self.toggle_mute()
        if self.volume > 0:
            self.volume -= 5
            if self.active_tab == 'device':
                self.redraw_volume_bar()
            self.timer2 = 200
            self.timed_event = lambda: set_sink_volume(self.active_sink[0],self.volume)
            root.title('Vol. - '+str(self.volume))

    def redraw_volume_bar(self):
        if self.muted == True:
            volume = self.muted_volume
            volcol = self.muted_volcol
        else:
            volume = self.volume
            volcol = self.volcol
        self.volume_canva.delete(ALL)
        if volume <= 100:
            self.volume_canva.create_rectangle(2, 2, volume*500/178.571, 300/10+2, fill=volcol[0], outline='')
        else:
            self.volume_canva.create_rectangle(2, 2, 100*500/178.571, 300/10+2, fill=volcol[0], outline='')
            self.volume_canva.create_rectangle(100*500/178.571, 2, volume*500/178.571-2, 300/10+2, fill=volcol[1], outline='')
        self.volume_canva.create_text((0,(300/10+4)/2),anchor=W, text=' '+str(volume),
                                      font= ('Liberation sans', 16, 'bold'), fill='white')
    def refresh(self):
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
    ## Refreshes Pulse Audio information
    def timer_task(self):
        self.timer -= 100
        if self.timer < 0:
            self.reset_timer()
            self.refresh()
        root.after(100, self.timer_task)
    ## Runs a function, usually volume change, a set amount of time after last input
    def timer2_task(self):
        if self.timer2 > 0:
            self.timer2 -= 20
            if self.timer2 == 0:
                self.timed_event()
                self.timer2 = -99
        root.after(20, self.timer2_task)
    def reset_timer(self):
        self.timer = 1000

    def toggle_mute(self,*arg):
        if self.muted == False:
            self.muted = True
            self.muted_volume, self.volume = self.volume, 0
            self.timer2 = 40
            self.timed_event = lambda: set_sink_volume(self.active_sink[0],0)
            gui_handler.reset_timer()
            self.redraw_volume_bar()
            self.bg_color = window_bgcol2
            for x in self.eq_button, self.frame2, self.sink_label, self.frame1, self.back_frame:
                x.configure(bg=self.bg_color)
            root.title("Muted")
        else:
            self.muted = False
            self.volume = self.muted_volume
            self.timer2 = 40
            self.timed_event = lambda: set_sink_volume(self.active_sink[0],self.volume)
            gui_handler.reset_timer()
            self.redraw_volume_bar()
            self.bg_color = window_bgcol
            for x in self.eq_button, self.frame2, self.sink_label, self.frame1, self.back_frame:
                x.configure(bg=self.bg_color)
            root.title("sPAGUI "+ver)

if __name__ == '__main__':
    ## Load settings
    default_sink = int(read_settings('default_sink=','0'))
    X_root = read_settings('X_root=','500')
    Y_root = read_settings('Y_root=','300')
    m_inputs = int(read_settings('m_inputs=',1))
    ## Global vars
    ver = '2'
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
    check_equalizer = '0'
    if os.path.exists('/usr/bin/qpaeq') == True:
        check_equalizer = 'qpaeq'
    if os.path.exists('/usr/local/bin/qpaeq') == True:
        check_equalizer = 'qpaeq'
    if os.path.exists('/usr/bin/pulseaudio-equalizer-gtk') == True:
        check_equalizer = 'pulse-eq-gtk'
    if os.path.exists('/usr/local/bin/pulseaudio-equalizer-gtk') == True:
        check_equalizer = 'pulse-eq-gtk'
    if check_equalizer == '0' :
        print ('Equalizer not found')
    else:
        print (check_equalizer,'found')

    root = Tk()
    root.title("sPAGUI "+ver)
    root.minsize(500,300)
    root.geometry('%sx%s' % (X_root,Y_root))
    maxsize = "5x5"

    def startup_task():
        global gui_handler, pac
        # set_winicon(root,'load/icon.ico')
        pac = PA_controller()
        gui_handler = GUI_handler()

    ##root.protocol('WM_DELETE_WINDOW', closewin)
    root.after(0, startup_task)
    root.mainloop()
