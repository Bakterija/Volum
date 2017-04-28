try:
    from Tkinter import Message
    from Tkinter import Label
except:
    from tkinter import Message
    from tkinter import Label


class MsgBinder(object):
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
            self.msg = Label(
                frame, image=self.img, width=width, background=self.bg)

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


def get_dict_item(dictio, item, default):
    for k, v in dictio.items():
        if k == item:
            return v
    return default
