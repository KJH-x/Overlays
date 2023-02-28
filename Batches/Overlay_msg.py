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
import re


def mouse_click(event: Event):
    """
    Get Mouse position when right/left mouse button pressed
    """
    global mouse_Δx, mouse_Δy, frame_x, frame_y
    print(f"[Action] mouse_click:\n{event}")
    print(f" - mouse_Δx: ", mouse_Δx := event.x)
    print(f" - mouse_Δy: ", mouse_Δy := event.y)
    print(f" - frame_x: ", frame_x := event.x_root)
    print(f" - frame_y: ", frame_y := event.y_root)

    if event.num == 3:
        # num==3 aka right click
        menu_layer01.post(frame_x, frame_y)


def mouse_drag(event: Event):
    """
    Move the frame when left mouse button pressed and dragged
    """
    global mw, txt, mouse_Δx, mouse_Δy
    print(f"[Action] mouse_drag:\n{event}")
    print(f" - frame_x: ", frame_x := event.x_root)
    print(f" - frame_y: ", frame_y := event.y_root)
    print(f" - move to +{frame_x - mouse_Δx}+{frame_y - mouse_Δy}")

    mw.geometry(f"+{frame_x - mouse_Δx}+{frame_y - mouse_Δy}")


def destroy_frame(event: Event):
    """
    Destroy and exit
    """
    print("[Command] Quit")
    exit()


def resize_frame(event: Event):
    """
    Enlarge when mouse wheel up or up arrow key pressed
    Shrink when mouse wheel down or down arrow key pressed
    """
    global mw, text_sizes, txt
    print(f"[Command] Resize_label:\n{event}")

    if event.delta > 0 or event.keysym == "Up":
        text_sizes[0] += int(0.2*text_sizes[0])
    elif event.delta < 0 or event.keysym == "Down":
        text_sizes[0] -= int(0.2*text_sizes[0])
    txt.configure(font=("华文中宋", text_sizes[0]))
    refresh_frame(event)


def change_content(event: Event):
    """
    Replace content when Ctrl+R pressed
    Append content to the end with return when Ctrl+Shift+R pressed
    Append content to the head with return when Ctrl+Shift+Alt+R pressed
    """
    global mw, txt, display_content
    print(f"[Command] Change_content:\n{event}")

    if event.state == 12:
        # aka. ctrl+
        # Replace Content
        if color := re.match(regexes['rgb1'], f"{pyperclip.paste()}"):
            # Color type, change bgcolor
            # #RGB #RRGGBB
            # #1F3 #8811DD
            txt.configure(bg=color.group())
            print(f" - Change background color to {color.group()}")
        elif color := re.match(regexes['rgb2'], f"{pyperclip.paste()}"):
            txt.configure(bg=f"#{color.group()}")
            print(f" - Change background color to #{color.group()}")
        else:
            display_content = f"{pyperclip.paste()}"
            print(f" - Change content to {display_content}")

    elif event.state == 13:
        # aka. ctrl+shift+
        # Append to the end
        display_content = f"{display_content}\n{pyperclip.paste()}"
        print(f" - Change content to {display_content}")

    elif event.state == 131085:
        # aka. ctrl+shift+alt
        # Append to the front
        display_content = f"{pyperclip.paste()}\n{display_content}"
        print(f" - Change content to {display_content}")

    txt.configure(text=display_content)
    refresh_frame(event)
    return


def refresh_frame(event: Event):
    """
    Refresh size and position when content or size change
    """
    global mw, txt
    print(f" - - refresh frame position")

    (CursorX, CursorY) = win32api.GetCursorPos()
    mw.geometry(f'+{abs(event.x - CursorX)}+{abs(event.y - CursorY)}')
    print(
        f" - - position set to {abs(event.x - CursorX)},{abs(event.y - CursorY)}"
    )


def change_alpha(event: Event):
    """
    Change opacity when Ctrl"""
    global mw, txt, alpha
    print(f"[Command] Change alpha:\n{event}")

    if event.delta > 0 or event.keysym == "Up":
        alpha += 0.05
    elif event.delta < 0 or event.keysym == "Down":
        alpha -= 0.05
    mw.attributes('-alpha', alpha)


def event_test(event: Event):
    print(f"{event}")
    return


regexes = {
    'rgb1': """#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})""",
    'rgb2': """([0-9a-fA-F]{6}|[0-9a-fA-F]{3})"""
    }
if __name__ == "__main__":

    os.system("chcp 65001 > nul")
    os.chdir(sys.path[0])
    title = f"[{str(pow(randint(1,10),randint(10,20)))}]"
    os.system(f"title {title}")

    text_sizes = [50, 20]
    alpha = 0.5
    display_content = pyperclip.paste()
    mw = tkinter.Tk()
    windll.shcore.SetProcessDpiAwareness(1)
    font_family = [("华文中宋", text_sizes[0]), ("华文中宋", text_sizes[1])]

    debug = 0
    if not debug:
        print(win32gui.ShowWindow(
            win32gui.FindWindow(0, title),
            win32con.HIDE_WINDOW
        ))

    mw.overrideredirect(1)
    mw.attributes('-alpha', alpha)
    mw.attributes("-topmost", 1)

    mw.bind('<Escape>', destroy_frame)
    mw.bind('<Control-c>', destroy_frame)
    mw.bind('<Control-C>', destroy_frame)
    mw.bind('<MouseWheel>', change_alpha)
    mw.bind('<Up>', change_alpha)
    mw.bind('<Down>', change_alpha)

    mw.bind('<Control-MouseWheel>', resize_frame)
    mw.bind('<Control-Up>', resize_frame)
    mw.bind('<Control-Down>', resize_frame)

    mw.bind('<Control-r>', change_content)
    mw.bind('<Control-R>', change_content)
    mw.bind('<Control-Shift-r>', change_content)
    mw.bind('<Control-Shift-R>', change_content)
    mw.bind('<Control-Shift-Alt-r>', change_content)
    mw.bind('<Control-Shift-Alt-R>', change_content)

    txt = tkinter.Label(mw, text=display_content, font=font_family[0],
                        bg="black", fg="white")
    txt.pack()
    txt.bind("<Button-1>", mouse_click)
    txt.bind("<Button-3>", mouse_click)
    txt.bind("<B1-Motion>", mouse_drag)

    menu_base = tkinter.Menu(mw, tearoff=False)
    menu_layer01 = tkinter.Menu(menu_base, tearoff=False)
    menu_layer02 = tkinter.Menu(menu_layer01, tearoff=False)
    # menu_layer03 = tkinter.Menu(menu_layer01, tearoff=False)

    menu_layer01.add_cascade(label='快捷键列表', menu=menu_layer02)
    # menu_layer01.add_cascade(label='命令', menu=menu_layer03)

    menu_layer02.configure(font=font_family[1])
    menu_layer01.configure(font=font_family[1])

    menu_layer02.add_command(label="[Esc]: 关闭")
    menu_layer02.add_command(label="[Ctrl+C]: 关闭")
    menu_layer02.add_command(label="[滚轮]: 改变不透明度")
    menu_layer02.add_command(label="[方向键上下]: 改变不透明度")
    menu_layer02.add_command(label="[Ctrl+滚轮]: 改变窗体大小")
    menu_layer02.add_command(label="[Ctrl+方向键上下]: 改变窗体大小")
    menu_layer02.add_command(label="[Ctrl+R]: 更新内容、更改背景颜色")
    menu_layer02.add_command(label="[Ctrl+Shift+R]: 追加内容")
    menu_layer02.add_command(label="[Ctrl+Shift+Alt+R]: 插入内容")

    (CursorX, CursorY) = win32api.GetCursorPos()
    mw.geometry(f"+{CursorX}+{CursorY}")
    mw.mainloop()

# Notes
# event.?_root == mouse absolute position ?
# mouse_Δ?     == mouse relative position ?
# event.
