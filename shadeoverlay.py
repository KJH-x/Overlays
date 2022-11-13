# encoding=utf-8
'''
Filename :overlay text.py
Description :...
Datatime :2022/09/30
Author :KJH
Version :v2.0
'''
import pyperclip
from ctypes import windll
import win32api
import win32gui
import win32con
import tkinter
from random import randint
from tkinter import Event
import os
import sys


def mouse_left_click(event: Event):
    """
    Get Mouse position when left mouse button pressed
    """
    global mousX, mousY
    print(f"mouse_left_click:\n{event}")

    mousX = event.x
    mousY = event.y


def mouse_drag(event: Event):
    """
    Move the frame when left mouse button pressed and dragged
    """
    global mw, mousX, mousY, txt
    print(f"mouse_drag:\n{event}")

    osx = mousX+txt.winfo_x()
    osy = mousY+txt.winfo_y()
    mw.geometry(f'+{event.x_root - osx}+{event.y_root - osy}')


def quit_command(event: Event):
    """
    Destroy and exit
    """
    print("quit")
    exit()


def resize_label(event: Event):
    """
    Enlarge when mouse wheel up or up arrow key pressed
    Shrink when mouse wheel down or down arrow key pressed
    """
    global mw, textsize, txt
    print(f"resize_label:\n{event}")

    if event.delta > 0 or event.keysym == "Up":
        textsize += int(0.2*textsize)
    elif event.delta < 0 or event.keysym == "Down":
        textsize -= int(0.2*textsize)
    txt.configure(font=("华文中宋", textsize))
    update_posit(event)


def change_content(event: Event):
    """
    Replace content when Ctrl+R pressed
    Append content to the end with return when Ctrl+Shift+R pressed
    Append content to the head with return when Ctrl+Shift+Alt+R pressed
    """
    global mw, txt, display_content
    print(f"change_content:\n{event}")

    return
    if event.state == 12:
        # aka. ctrl+
        display_content = f"{pyperclip.paste()}"
    elif event.state == 13:
        # aka. ctrl+shift+
        display_content = f"{display_content}\n{pyperclip.paste()}"
    elif event.state == 131085:
        # aka. ctrl+shift+alt
        display_content = f"{pyperclip.paste()}\n{display_content}"
    txt.configure(text=display_content)
    update_posit(event)


def update_posit(event: Event):
    """
    Refresh size and position when content or size change
    """
    global mw, txt
    print(f"---update_posit")

    (CursorX, CursorY) = win32api.GetCursorPos()
    mw.geometry(f'+{abs(event.x - CursorX)}+{abs(event.y - CursorY)}')
    print(
        f"---position set to {abs(event.x - CursorX)},{abs(event.y - CursorY)}"
    )


def change_alpha(event: Event):
    """
    Change opacity when Ctrl
    """
    global mw, txt, alpha
    print(f"change_alpha:\n{event}")

    if event.delta > 0 or event.keysym == "Up":
        alpha += 0.05
        alpha = min(alpha, 1)
    elif event.delta < 0 or event.keysym == "Down":
        alpha -= 0.05
        alpha = max(alpha, 0.05)
    mw.attributes('-alpha', alpha)


def event_test(event: Event):
    print(f"{event}")
    return


def topmost(event: Event):
    mw.attributes("-topmost", 0)
    mw.geometry(f"3840x2160+0+0")
    return


if __name__ == "__main__":

    os.system("chcp 65001")
    os.chdir(sys.path[0])
    title = f"[{str(pow(randint(1,10),randint(10,20)))}]"
    os.system(f"title {title}")

    textsize = 50
    alpha = 0.5
    display_content = pyperclip.paste()
    mw = tkinter.Tk()
    windll.shcore.SetProcessDpiAwareness(1)
    font_family1 = ("华文中宋", textsize)

    debug = 1
    if not debug:
        win32gui.ShowWindow(
            win32gui.FindWindow(0, title),
            win32con.HIDE_WINDOW
        )

    mw.overrideredirect(1)
    mw.attributes("-alpha", alpha)
    mw.attributes("-topmost", 1)
    mw.bind("<Escape>", quit_command)
    mw.bind("<Control-c>", quit_command)
    mw.bind("<Control-C>", quit_command)
    mw.bind("<MouseWheel>", change_alpha)
    mw.bind("<Up>", change_alpha)
    mw.bind("<Down>", change_alpha)

    mw.bind("<Control-MouseWheel>", resize_label)
    mw.bind("<Control-Up>", resize_label)
    mw.bind("<Control-Down>", resize_label)
    mw.bind("<Control-t>", topmost)
    mw.bind("<Control-T>", topmost)

    # mw.bind("<Control-r>", change_content)
    # mw.bind("<Control-R>", change_content)
    # mw.bind("<Control-Shift-r>", change_content)
    # mw.bind("<Control-Shift-R>", change_content)
    # mw.bind("<Control-Shift-Alt-r>", change_content)
    # mw.bind("<Control-Shift-Alt-R>", change_content)
    # mw.bind("<Double-Button-1>", change_content)

    txt = tkinter.Label(mw, text=display_content, font=font_family1,
                        bg="black", fg="white")
    # txt.pack()
    # mw.bind("<Button-1>", mouse_left_click)
    # mw.bind("<B1-Motion>", mouse_drag)
    mw.config(background="black")

    (CursorX, CursorY) = win32api.GetCursorPos()
    mw.geometry(f"3840x2160+0+0")
    mw.mainloop()
