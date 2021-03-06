#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 6.0.1
#  in conjunction with Tcl version 8.6
#    Mar 21, 2021 03:14:50 PM +0200  platform: Windows NT

import sys
import socket
sys.path.insert(0, 'C:/Users/Shalev/Desktop/תיקיות/Python Project/GUIS/register')
import register
sys.path.insert(0, 'C:/Users/Shalev/Desktop/תיקיות/Python Project/GUIS/login')
import login

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

from GUIS.authentication import authentication_support

def on_closing(my_socket, root):
    my_socket.shutdown(socket.SHUT_RDWR)
    my_socket.close()
    root.destroy()

def vp_start_gui(my_socket):
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Authentication (my_socket, root)
    authentication_support.init(root, top)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(my_socket, root))
    root.mainloop()

w = None
def create_Authentication(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Authentication(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = Authentication (w)
    authentication_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Authentication():
    global w
    w.destroy()
    w = None

def open_register(top, my_socket):
    top.destroy()
    register.vp_start_gui(my_socket)

def open_login(top, my_socket):
    top.destroy()
    login.vp_start_gui(my_socket)

class Authentication:
    def __init__(self, my_socket, top=None):
        self.my_socket = my_socket
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("600x450+615+242")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("Authentication")
        top.configure(background="#d9d9d9")

        self.Login_Button = tk.Button(top)
        self.Login_Button.place(relx=0.567, rely=0.4, height=24, width=107)
        self.Login_Button.configure(activebackground="#ececec")
        self.Login_Button.configure(activeforeground="#000000")
        self.Login_Button.configure(background="#d9d9d9")
        self.Login_Button.configure(cursor="hand2")
        self.Login_Button.configure(disabledforeground="#a3a3a3")
        self.Login_Button.configure(foreground="#000000")
        self.Login_Button.configure(highlightbackground="#d9d9d9")
        self.Login_Button.configure(highlightcolor="black")
        self.Login_Button.configure(pady="0")
        self.Login_Button.configure(text='''Login''')
        self.Login_Button.configure(command=lambda: open_login(top, self.my_socket))

        self.Welcome = tk.Label(top)
        self.Welcome.place(relx=0.433, rely=0.311, height=21, width=74)
        self.Welcome.configure(background="#d9d9d9")
        self.Welcome.configure(disabledforeground="#a3a3a3")
        self.Welcome.configure(foreground="#000000")
        self.Welcome.configure(text='''Welcome''')

        self.Register_Button = tk.Button(top)
        self.Register_Button.place(relx=0.25, rely=0.4, height=24, width=107)
        self.Register_Button.configure(activebackground="#ececec")
        self.Register_Button.configure(activeforeground="#000000")
        self.Register_Button.configure(background="#d9d9d9")
        self.Register_Button.configure(cursor="hand2")
        self.Register_Button.configure(disabledforeground="#a3a3a3")
        self.Register_Button.configure(foreground="#000000")
        self.Register_Button.configure(highlightbackground="#d9d9d9")
        self.Register_Button.configure(highlightcolor="black")
        self.Register_Button.configure(pady="0")
        self.Register_Button.configure(text='''Register''')
        self.Register_Button.configure(command=lambda: open_register(top, self.my_socket))

if __name__ == '__main__':
    vp_start_gui()

