import tkinter
import win32api
import ctypes
import pyperclip


def MouseDown(event):
    global mousX, mousY

    mousX = event.x
    mousY = event.y


def MouseMoveW1(event):
    global mw, mousX, mousY, txt

    osx = mousX+txt.winfo_x()
    osy = mousY+txt.winfo_y()
    mw.geometry(f'+{event.x_root - osx}+{event.y_root - osy}')


def keyquit(event):
    print("quit")
    exit()


def wheelchange(event):
    global mw, textsize, txt
    print(f"wheel:\n{event}")
    if event.delta > 0:
        textsize += int(0.2*textsize)
    else:
        textsize -= int(0.2*textsize)

    txt.configure(font=("华文中宋", textsize))

    update_posit(event)


def refreshcontent(event):
    global mw, txt
    print(f"Update content!\n{event}\n")
    txt.configure(text=str(pyperclip.paste()))

    update_posit(event)


def update_posit(event):
    global mw, txt
    (CursorX, CursorY) = win32api.GetCursorPos()
    mw.geometry(f'+{abs(event.x - CursorX)}+{abs(event.y - CursorY)}')
    print(f"position set to {abs(event.x - CursorX)},{abs(event.y - CursorY)}")


textsize = 50

display_content = str(pyperclip.paste())
mw = tkinter.Tk()
ctypes.windll.shcore.SetProcessDpiAwareness(1)
font_family1 = ("华文中宋", textsize)

mw.overrideredirect(1)
mw.attributes('-alpha', 0.7)
mw.attributes("-topmost", 1)
mw.bind("<Escape>", keyquit)
mw.bind('<Control-c>', keyquit)
mw.bind('<Control-C>', keyquit)
mw.bind('<MouseWheel>', wheelchange)
mw.bind('<Control-r>', refreshcontent)
mw.bind('<Control-R>', refreshcontent)

txt = tkinter.Label(mw, text=display_content, font=font_family1,
                    bg="black", fg="white")
txt.pack()
txt.bind("<Button-1>", MouseDown)
txt.bind("<B1-Motion>", MouseMoveW1)


(CursorX, CursorY) = win32api.GetCursorPos()
mw.geometry(f"+{CursorX}+{CursorY}")
mw.mainloop()
