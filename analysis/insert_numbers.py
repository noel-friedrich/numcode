import json

nums = []

while True:
    inp = input("num: ")
    if inp == "stop":
        break
    if len(inp) != 8:
        print("oops. not 8 long!")
        continue
    nums.append(inp)

print(json.dumps(nums))