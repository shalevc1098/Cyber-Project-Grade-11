import socket

last_chat_id = 1
counter = 0

def get_last_chat_id():
    global last_chat_id, counter
    if counter == 2:
        last_chat_id += 1
        counter = 0
    else:
        counter += 1
    return last_chat_id