temp = {}

temp["1"] = "Hello"
temp["2"] = "World"

for key in temp:
    print(f"{key}: {temp[key]}")

del temp["2"]

for key in temp:
    print(f"{key}: {temp[key]}")