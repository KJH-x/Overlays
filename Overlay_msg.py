# encoding=utf-8
'''
Filename :overlay text.py
Description :N/A
Datatime :2022/09/18
Author :KJH
Version :v1.0
'''
import pyperclip
import ctypes
import win32api
import tkinter
import os
import sys
os.system("chcp 65001")
os.chdir(sys.path[0])


def MouseDown(event):
    global mousX, mousY

    mousX = event.x
    mousY = event.y


def MouseMoveW1(event):
    global mw, mousX, mousY, txt

    osx = mousX+txt.winfo_x()
    osy = mousY+txt.winfo_y()
    mw.geometry(f'+{event.x_root - osx}+{event.y_root - osy}')


def quit_command(event):
    print("quit")
    exit()


def resize(event):
    global mw, textsize, txt
    print(f"wheel:\n{event}")
    if event.delta > 0 or event.keysym == "Up":
        textsize += int(0.2*textsize)
    elif event.delta < 0 or event.keysym == "Down":
        textsize -= int(0.2*textsize)

    txt.configure(font=("华文中宋", textsize))

    update_posit(event)


def update_content(event):
    global mw, txt
    print(f"Update content!\n{event}\n")
    txt.configure(text=str(pyperclip.paste()))

    update_posit(event)


def update_posit(event):
    global mw, txt
    (CursorX, CursorY) = win32api.GetCursorPos()
    mw.geometry(f'+{abs(event.x - CursorX)}+{abs(event.y - CursorY)}')
    print(f"position set to {abs(event.x - CursorX)},{abs(event.y - CursorY)}")


def alpha_change(event):
    global mw, txt, alpha
    print("control+wheel", event)
    if event.delta > 0 or event.keysym == "Up":
        alpha += 0.05
    elif event.delta < 0 or event.keysym == "Down":
        alpha -= 0.05

    mw.attributes('-alpha', alpha)


textsize = 50
alpha = 0.5
display_content = str(pyperclip.paste())
mw = tkinter.Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
font_family1 = ("华文中宋", textsize)

mw.overrideredirect(1)
mw.attributes('-alpha', alpha)
mw.attributes("-topmost", 1)
mw.bind("<Escape>", quit_command)
mw.bind('<Control-c>', quit_command)
mw.bind('<Control-C>', quit_command)
mw.bind('<MouseWheel>', alpha_change)
mw.bind('<Up>', alpha_change)
mw.bind('<Down>', alpha_change)

mw.bind('<Control-MouseWheel>', resize)
mw.bind('<Control-Up>', resize)
mw.bind('<Control-Down>', resize)

mw.bind('<Control-r>', update_content)
mw.bind('<Control-R>', update_content)

txt = tkinter.Label(mw, text=display_content, font=font_family1,
                    bg="black", fg="white")
txt.pack()
txt.bind("<Button-1>", MouseDown)
txt.bind("<B1-Motion>", MouseMoveW1)


(CursorX, CursorY) = win32api.GetCursorPos()
mw.geometry(f"+{CursorX}+{CursorY}")
mw.mainloop()
