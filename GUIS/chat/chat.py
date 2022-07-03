import threading
import tkinter
import socket
import queue
import sys

messages = queue.Queue()
running = True

def send(my_socket, my_msg, username, chat_id, event=None):  # event is passed by binders.
    """Handles sending of messages."""
    can_send = False
    msg = my_msg.get()
    for char in msg:
        if ord(char) != 32:
            can_send = True
            break
    if can_send:
        my_socket.send(f"chat,addmessage,{chat_id},{username},{msg}".encode())

def receive(my_socket, username, top, msg_list):
    """Handles receiving of messages."""
    global running
    while running:
        top.update()
        while not messages.empty():
            args = messages.get()
            if args[0] == "chat":
                if args[1] == "addmessage":
                    try:
                        msg_list.insert(tkinter.END, args[2])
                    except OSError:  # Possibly client has left the chat.
                        pass
                msg_list.see("end")
    top.destroy()

def no_op(event):
    return "break"

def on_closing(my_socket, top, chat_id):
    global running
    if running:
        return

def set_running(value):
    global running
    running = value

def start(my_socket, username, chat_id):
    top = tkinter.Tk()
    top.title("Chat")
    
    top.protocol("WM_DELETE_WINDOW", lambda: on_closing(my_socket, top, chat_id))
    top.resizable(False, False)

    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar(top)  # For the messages to be sent.
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set, selectmode="")
    msg_list.bind("<Button-1>", no_op)
    msg_list.bind("<Double-1>", no_op)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg, justify='center')
    entry_field.bind("<Return>", lambda event: send(my_socket, my_msg, username, chat_id, event))
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=lambda: send(my_socket, my_msg, username, chat_id))
    send_button.pack()

    receive(my_socket, username, top, msg_list)