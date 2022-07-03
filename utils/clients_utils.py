global_connected = []
tictactoe_queue = {}
fourinarow_queue = []

def append_to_global_connected(value):
    global global_connected
    global_connected.append(value)

def append_to_tictactoe_queue(key, value):
    global tictactoe_queue
    tictactoe_queue[key] = value

def append_to_fourinarow_queue(value):
    global fourinarow_queue
    fourinarow_queue.append(value)

def get_global_connected():
    global global_connected
    return global_connected

def get_tictactoe_queue():
    global tictactoe_queue
    return tictactoe_queue

def get_fourinarow_queue():
    global fourinarow_queue
    return fourinarow_queue

def remove_from_global_connected(value):
    global global_connected
    global_connected.remove(value)

def remove_from_tictactoe_queue(key):
    global tictactoe_queue
    if key in tictactoe_queue[key]:
        del tictactoe_queue[key]

def remove_from_fourinarow_queue(value):
    global fourinarow_queue
    fourinarow_queue.remove(value)