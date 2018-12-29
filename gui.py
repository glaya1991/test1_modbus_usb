import random
import time
import  threading
from tkinter import Tk as tk
from tkinter import Button as btn
from tkinter import Entry as ent
from tkinter import Label as lbl
from tkinter import Radiobutton as rd_btn
from tkinter import Checkbutton as chk_btn
from tkinter import Text as memo
from tkinter import IntVar

from tkinter import END, INSERT, SEL

import colors_def

# properties (arguments)
#   relief = "x":   x= flat, groove, raised, ridge, solid, or sunken
#   sticky = "x":   W,E,S(низ),N(верх) -- align of widget to certain side of grid-box, if widget situated several rows/columns
#   anchor = "x":   n,ne,e,s,se,s,sw,w,nw,center -- align of text, picture in widget
#   justify = "x":  left,right,center -- align of multiple lines of text in widget

root = tk()
btn1 = btn(master=root) # or btn1 = btn(master=root, text="press", background="ivory4", foreground="black")
btn2 = btn(master=root)
btn3 = btn(master=root)
ent1 = ent(master=root) # or ent1 = ent(master=root, background="white", foreground="black")
memo1 = memo(master=root)
memo2 = memo(master=root)
lbl1 = lbl(master=root)
rd_btn1 = rd_btn(master=root)
rd_btn2 = rd_btn(master=root)

color_SysButFace = "SystemButtonFace"
color_SysButHL = "SystemButtonHighlight"
color_SysButSh = "SystemButtonShadow"
color_SysMenu = "SystemMenu"



def create_place():
    # test
    print(root.keys())

    # location on master with .place()
    root_width = 640
    root_height = 400
    btn_width = 60
    btn_height = 20
    root.geometry("{:d}x{:d}+0+0".format(root_width, root_height))

    # Установить цветовую палитру на все виджеты сразу (кроме, возможно, специальных настроек)
    root.tk_setPalette(background=color_SysMenu, foreground="blue", activebackground=color_SysButSh, activeforeground="red")
    color_bg = root.cget("bg")
    color_fg = btn1.cget("fg")

    btn1.config(text="send")
    btn1.place(x=10, y=10, width=btn_width, height=btn_height)

    btn2.config(text="clear")
    btn2.place(x=100, y=10, width=btn_width, height=btn_height)

    lbl1.config(text="label", bg = color_bg, fg=color_fg, anchor="w")
    lbl1.place(x = 10, y = btn_height+20, width = root_width-10*2)

    var1 = IntVar()
    rd_btn1.config(text="test1", variable=var1, value=1)
    rd_btn1.place(x=root_width-80, y=10)

    rd_btn2.config(text="test2", variable=var1, value=2)
    rd_btn2.place(x=root_width-80, y=30)

    # var1.set(1)

    memo1.config(bg="white", fg=color_fg, borderwidth=2, relief="sunken")
    memo1.place(x=10, y=80, width=300, height=(root_height-80)-10*2)

    memo2.config(bg="white", fg=color_fg, borderwidth=2, relief="sunken")
    memo2.place(x=320, y=80, width=300, height=(root_height-80)-10*2)


def create_grid():
    # location on master with .grid()
    # row -- ряд
    # column -- столбец
    # columnspan -- сколько столбцов занимает виджет
    # rowspan -- сколько строк занимает виджет
    # sticky = W,E,S(низ),N(верх) -- прилегание к определенной границе ячейки, если она занимкат несколько столбцов/строк

    # ширина столбца равняется максимальной ширине входящего в него виджета
    # с выстотой похоже дела обстоят аналогично

    root_width =200
    root_height = 200
    root.geometry("{:d}x{:d}+0+0".format(root_width, root_height))

    btn1.config(text="1", background="ivory3", foreground="black")
    btn1.grid(row=0, column=0, rowspan=1, columnspan=1, ipadx=12)

    btn2.config(text="2", background="ivory3", foreground="black")
    btn2.grid(row=0, column=1, rowspan=1, columnspan=1, ipadx=4)

    btn3.config(text="3", background="plum3", foreground="black")
    btn3.grid(row=0, column=3, rowspan=2, ipady=5, sticky="S")

    ent1.config(background="white", foreground="black")
    ent1.grid(row=1, column=0, columnspan=1)

    memo1.config(height=5, width=10)    # "height" in case of text-widget: 1 unit = 1 text-height
    memo1.grid(row=2, column=0)

def create_pack():
    root_width =200
    root_height = 200
    root.geometry("{:d}x{:d}+0+0".format(root_width, root_height))

    btn1.config(text="1", background="ivory3", foreground="black")
    btn1.pack(side="top", ipadx=4)

    btn2.config(text="2", background="ivory3", foreground="black")
    btn2.pack(side="top")

    memo1.config(height=5, width=10)    # "height" in case of text-widget: 1 unit = 1 text-height
    memo1.pack(side="bottom")

    return

def start():
    root.mainloop()
