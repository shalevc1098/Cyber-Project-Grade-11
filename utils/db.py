import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

def check_request(request):
    request = str(request)
    command = request.split(",")[1]
    database = client["python_project_2021"]
    if command == "register":
        users = database["users"]
        username = request.split(",")[2]
        password = request.split(",")[3]
        exists = users.find_one({"username": username}) != None
        if not exists:
            users.insert_one({"username": username, "password": password})
            return f"{username} registered successfully"
        else:
            return f"{username} already registered"
    elif command == "login":
        users = database["users"]
        username = request.split(",")[2]
        password = request.split(",")[3]
        exists = users.find_one({"username": username}) != None
        if exists:
            user_password = users.find_one({"username": username}, {"_id": 0, "password": 1})["password"]
            if password == user_password:
                return f"{username} logged successfully"
            else:
                return f"password is incorrect"
        else:
            return f"{username} is not registered"