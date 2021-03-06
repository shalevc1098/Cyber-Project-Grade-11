#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 6.0.1
#  in conjunction with Tcl version 8.6
#    Mar 21, 2021 03:14:50 PM +0200  platform: Windows NT

import os
import sys
import socket
import threading
import importlib
#print(os.path.abspath(os.path.join(f'{os.getcwd()}', '..')))
sys.path.insert(0, 'C:/Users/Shalev/Desktop/תיקיות/Python Project/GUIS/games/fourinarow/game')
import fourinarow
import queue

messages = queue.Queue()

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

import fourinarow_queue_support

running = True
canclose = False

def get_can_close():
    global canclose
    return canclose

def set_can_close(val):
    global canclose
    canclose = val

def loop(my_socket):
    global running
    while running:
        try:
            response = my_socket.recv(1024).decode()
            messages.put(response)
            args = response.split(",")
            if args[0] == "start_fourinarow":
                running = False
        except:
            running = False

def client_handler(my_socket, top, label, username, geometry):
    global running
    while running:
        top.update()
        while not messages.empty():
            args = messages.get().split(",")
            if args[0] == "fourinarow_queue_addtoqueue" or args[0] == "fourinarow_queue_removefromqueue":
               label.configure(text=args[1])
            elif args[0] == "start_fourinarow":
                top.withdraw()
                running = False
                importlib.reload(fourinarow)
                fourinarow.start(int(args[1]), int(args[2]), my_socket, username, geometry)
        
def on_closing(my_socket, root):
    global running, canclose
    canclose = True
    running = False
    my_socket.shutdown(socket.SHUT_RDWR)
    my_socket.close()
    root.destroy()

def vp_start_gui(my_socket, username, geometry):
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = FourInARow_Queue (my_socket, username, geometry, root)
    fourinarow_queue_support.init(root, top)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(my_socket, root))
    a = threading.Thread(target=loop, args=(my_socket,))
    a.start()
    client_handler(my_socket, root, top.get_top(), username, geometry)

w = None
def create_FourInARow_Queue(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_FourInARow_Queue(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = FourInARow_Queue (w)
    fourinarow_queue_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_FourInARow_Queue():
    global w
    w.destroy()
    w = None

class FourInARow_Queue:
    def __init__(self, my_socket, username, geometry, top=None):
        self.my_socket = my_socket
        self.username = username
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry(geometry)
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("Four In A Row - Queue")
        top.configure(background="#d9d9d9")

        self.FourInARow_Queue = tk.Label(top)
        self.FourInARow_Queue.place(relx=0.433, rely=0.311, height=21, width=74)
        self.FourInARow_Queue.configure(background="#d9d9d9")
        self.FourInARow_Queue.configure(disabledforeground="#a3a3a3")
        self.FourInARow_Queue.configure(foreground="#000000")
        self.FourInARow_Queue.configure(text=f'''In Queue: 0''')

        my_socket.send("fourinarow_queue,addtoqueue".encode())

    def get_top(self):
        return self.FourInARow_Queue

if __name__ == '__main__':
    vp_start_gui()

