import json

test = {}

test["1"] = "Hello"
test["2"] = "World"

lst = list(test.keys())
string = json.dumps(lst)

print(string)
print(type(string))

converted = json.loads(string)

print(converted)
print(type(converted))
print(converted[0])
print(converted[1])