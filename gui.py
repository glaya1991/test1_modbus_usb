import random
import time
import threading

from tkinter import Tk as tk
from tkinter import Button as btn
from tkinter import Entry as ent
from tkinter import Label as lbl
from tkinter import Radiobutton as rd_btn
from tkinter import Checkbutton as chk_btn
from tkinter import Text as memo
from tkinter import IntVar, StringVar
from tkinter import Scrollbar
from tkinter import Menu as menu
from tkinter import Event
from tkinter import Canvas

from tkinter import END, INSERT, SEL

import colors_def



# properties (arguments)
#   relief = "x":   x= flat, groove, raised, ridge, solid, or sunken
#   sticky = "x":   W,E,S(низ),N(верх) -- align of widget to certain side of grid-box, if widget situated several rows/columns
#   anchor = "x":   n,ne,e,s,se,s,sw,w,nw,center -- align of text, picture in widget
#   justify = "x":  left,right,center -- align of multiple lines of text in widget


# events and callbacks:

# <Button-1> Button 1 is the leftmost button, button 2 is the middle button
# (where available), and button 3 the rightmost button.
#
# <Button-1>, <ButtonPress-1>, and <1> are all synonyms.
#
# For mouse wheel support under Linux, use Button-4 (scroll
# up) and Button-5 (scroll down)
#
# <B1-Motion> The mouse is moved, with mouse button 1 being held down (use
# B2 for the middle button, B3 for the right button).
#
# <ButtonRelease-1> Button 1 was released. This is probably a better choice in
# most cases than the Button event, because if the user
# accidentally presses the button, they can move the mouse
# off the widget to avoid setting off the event.
#
# <Double-Button-1> Button 1 was double clicked. You can use Double or Triple as
# prefixes.
#
# <Enter> The mouse pointer entered the widget (this event doesn’t mean
# that the user pressed the Enter key!).
#
# <Leave> The mouse pointer left the widget.
#
# <FocusIn> Keyboard focus was moved to this widget, or to a child of
# this widget.
#
# <FocusOut> Keyboard focus was moved from this widget to another widget.
#
# <Return> The user pressed the Enter key. For an ordinary 102-key
# PC-style keyboard, the special keys are Cancel (the Break
# key), BackSpace, Tab, Return(the Enter key), Shift_L (any
# Shift key), Control_L (any Control key), Alt_L (any Alt key),
# Pause, Caps_Lock, Escape, Prior (Page Up), Next (Page Down),
# End, Home, Left, Up, Right, Down, Print, Insert, Delete, F1,
# F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, Num_Lock, and
# Scroll_Lock.
#
# <Key> The user pressed any key. The key is provided in the char
# member of the event object passed to the callback (this is an
# empty string for special keys).
#
# a The user typed an “a”. Most printable characters can be used
# as is. The exceptions are space (<space>) and less than
# (<less>). Note that 1 is a keyboard binding, while <1> is a
# button binding.
#
# <Shift-Up> The user pressed the Up arrow, while holding the Shift key
# pressed. You can use prefixes like Alt, Shift, and Control.
#
# <Configure> The widget changed size (or location, on some platforms). The
# new size is provided in the width and height attributes of
# the event object passed to the callback.
#
# <Activate> A widget is changing from being inactive to being active.
# This refers to changes in the state option of a widget such
# as a button changing from inactive (grayed out) to active.
#
#
# <Deactivate> A widget is changing from being active to being inactive.
# This refers to changes in the state option of a widget such
# as a radiobutton changing from active to inactive (grayed out).
#
# <Destroy> A widget is being destroyed.
#
# <Expose> This event occurs whenever at least some part of your
# application or widget becomes visible after having been
# covered up by another window.
#
# <KeyRelease> The user let up on a key.
#
# <Map> A widget is being mapped, that is, made visible in the
# application. This will happen, for example, when you call the
# widget's .grid() method.
#
# <Motion> The user moved the mouse pointer entirely within a widget.
#
# <MouseWheel> The user moved the mouse wheel up or down. At present, this
# binding works on Windows and MacOS, but not under Linux.
#
# <Unmap> A widget is being unmapped and is no longer visible.
#
# <Visibility> Happens when at least some part of the application window
# becomes visible on the screen.

root = tk()
btn_get_msg = btn(master=root) # or btn1 = btn(master=root, text="press", background="ivory4", foreground="black")
btn_send = btn(master=root)
btn_clr1 = btn(master=root)
btn_clr2 = btn(master=root)
ent1 = ent(master=root) # or ent1 = ent(master=root, background="white", foreground="black")
ent2 = ent(master=root)
ent3 = ent(master=root)
ent4 = ent(master=root)

memo_msg = memo(master=root)
memo_send = memo(master=root)
memo_recv = memo(master=root)
scrolly_recv = Scrollbar(master=root)

lbl1 = lbl(master=root)
lbl2 = lbl(master=root)
lbl3 = lbl(master=root)
lbl4 = lbl(master=root)
rd_btn1 = rd_btn(master=root)
rd_btn2 = rd_btn(master=root)
rd_btn3 = rd_btn(master=root)
var1 = StringVar()

canvas1 = Canvas(master=root)

copy_buffer = ""

color_SysButFace = "SystemButtonFace"
color_SysButHL = "SystemButtonHighlight"
color_SysButSh = "SystemButtonShadow"
color_SysMenu = "SystemMenu"

def create_place():
    # test
    print(root.keys())
    print()

    # location on master with .place()
    root_wdt = 640
    root_hgh = 480
    btn_wdt = 60
    btn_hgh = 20
    ent_wdt = 60
    ent_hgh = 20
    memo_wdt = 290
    root.geometry("{:d}x{:d}+0+0".format(root_wdt, root_hgh))


    # Установить цветовую палитру на все виджеты сразу (кроме, возможно, специальных настроек)
    root.tk_setPalette(background=color_SysMenu, foreground="blue", activebackground=color_SysButSh, activeforeground="red", highlightBackground="maroon")
    color_bg = root.cget("bg")
    color_fg = btn_send.cget("fg")


    lbl1.config(text="id", bg=color_bg, fg=color_fg, anchor="w")
    lbl1.place(x=10, y=15)
    lbl2.config(text="func", bg=color_bg, fg=color_fg, anchor="w")
    lbl2.place(x=100, y=15)
    lbl3.config(text="addr", bg=color_bg, fg=color_fg, anchor="w")
    lbl3.place(x=190, y=15)
    lbl4.config(text="num", bg=color_bg, fg=color_fg, anchor="w")
    lbl4.place(x=280, y=15)

    ent1.config(bg="white")
    ent1.insert(0, "FF")
    ent1.place(x=10, y=40, width=ent_wdt, height=ent_hgh)
    ent2.config(bg="white")
    ent2.insert(0, "3")
    ent2.place(x=100, y=40, width=ent_wdt, height=ent_hgh)
    ent3.config(bg="white")
    ent3.insert(0, "0")
    ent3.place(x=190, y=40, width=ent_wdt, height=ent_hgh)
    ent4.config(bg="white")
    ent4.insert(0, "1")
    ent4.place(x=280, y=40, width=ent_wdt, height=ent_hgh)

    btn_get_msg.config(text="get_msg")
    btn_get_msg.place(x=370, y=40, width=btn_wdt, height=btn_hgh)

    memo_msg.config(bg="white", fg=color_fg, borderwidth=2, relief="sunken")
    memo_msg.place(x=10, y=70, width=340-10, height=60)

    memo_msg.bind("<Button-3>", (callback_memo_click_right))

    var1.set("1")

    rd_btn1.config(text="hex", variable=var1, value="1")
    rd_btn1.place(x=root_wdt-80, y=40)

    rd_btn2.config(text="dec", variable=var1, value="2")
    rd_btn2.place(x=root_wdt-80, y=60)

    rd_btn3.config(text="sym", variable=var1, value="3")
    rd_btn3.place(x=root_wdt-80, y=80)

    memo_send.config(bg="white", fg=color_fg, borderwidth=2, relief="sunken")
    memo_send.place(x=10, y=160, width=memo_wdt, height=100)

    memo_send.bind("<Button-3>", (callback_memo_click_right))

    memo_recv.config(bg="white", fg=color_fg, borderwidth=2, relief="sunken")
    memo_recv.config(yscrollcommand=scrolly_recv.set)
    memo_recv.place(x=memo_wdt + 20, y=160, width=memo_wdt, height=(root_hgh - 160) - 40)

    memo_recv.bind("<Button-3>", (callback_memo_click_right))

    scrolly_recv.config(command=memo_recv.yview, background="red")
    scrolly_recv.place(x=2*memo_wdt + 20, y=160, height=(root_hgh - 160) - 40)

    btn_send.config(text="send")
    btn_send.place(x=10, y=270, width=btn_wdt, height=btn_hgh)

    btn_clr1.config(text="clr")
    btn_clr1.place(x=memo_wdt - btn_wdt, y=270, width=btn_wdt, height=btn_hgh)

    btn_clr2.config(text="clr")
    btn_clr2.place(x=2 * memo_wdt + 20 - btn_wdt, y=root_hgh - 40 + 10, width=btn_wdt, height=btn_hgh)

    color1 = "#00007878D7D7"
    color2 = "#0078D7"
    canvas1.config(bg="#FFFFFF")
    canvas1.create_rectangle(0,0,50,50, fill=color1, outline="")
    canvas1.create_rectangle(50,0,100,50, fill=color2, outline="")
    canvas1.place(x=10, y=320, width=100, height=50)


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

    btn_send.config(text="1", background="ivory3", foreground="black")
    btn_send.grid(row=0, column=0, rowspan=1, columnspan=1, ipadx=12)

    btn_clr1.config(text="2", background="ivory3", foreground="black")
    btn_clr1.grid(row=0, column=1, rowspan=1, columnspan=1, ipadx=4)

    btn_clr2.config(text="3", background="plum3", foreground="black")
    btn_clr2.grid(row=0, column=3, rowspan=2, ipady=5, sticky="S")

    ent1.config(background="white", foreground="black")
    ent1.grid(row=1, column=0, columnspan=1)

    memo_send.config(height=5, width=10)    # "height" in case of text-widget: 1 unit = 1 text-height
    memo_send.grid(row=2, column=0)

def create_pack():
    root_width =200
    root_height = 200
    root.geometry("{:d}x{:d}+0+0".format(root_width, root_height))

    btn_send.config(text="1", background="ivory3", foreground="black")
    btn_send.pack(side="top", ipadx=4)

    btn_clr1.config(text="2", background="ivory3", foreground="black")
    btn_clr1.pack(side="top")

    memo_send.config(height=5, width=10)    # "height" in case of text-widget: 1 unit = 1 text-height
    memo_send.pack(side="bottom")

    return


def memo_select(widget):
    widget.tag_add(SEL, 1.0, END)
    widget.focus_set()
    return

def memo_get(widget):
    global copy_buffer
    copy_buffer = widget.get(1.0, END)
    return

def memo_insert(widget):
    global copy_buffer
    widget.insert(INSERT, copy_buffer)
    return

def callback_memo_click_right(event):
    menu1 = menu(tearoff=0)
    menu1.add_command(label="Copy", command=lambda: memo_get(event.widget))
    menu1.add_command(label="Paste", command=lambda: memo_insert(event.widget))
    menu1.add_command(label="Select", command=lambda: memo_select(event.widget))
    menu1.post(event.x_root, event.y_root)
    print("clicked at ", event.x_root, event.y_root)
    return


def start():
    root.mainloop()
