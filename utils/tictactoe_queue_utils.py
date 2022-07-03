in_queue = 0
def check_request(request):
    request = str(request)
    command = request.split(",")[1]
    global in_queue
    if command == "addtoqueue":
        in_queue += 1
        return f"tictactoe_queue_addtoqueue,In Queue: {in_queue}"
    elif command == "removefromqueue":
        in_queue -= 1
        return f"tictactoe_queue_removefromqueue,In Queue: {in_queue}"