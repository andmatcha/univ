people = [
    {"name": "Taro", "height": 1.7, "weight": 52},
    {"name": "Jiro", "height": 1.6, "weight": 75},
    {"name": "Ichiro", "height": 1.8, "weight": 63},
]

for person in people:
    bmi = person["weight"] / person["height"] ** 2
    if bmi < 18.5:
        print(person["name"] + ": やせ型")
    elif bmi < 25:
        print(person["name"] + ": 標準")
    else:
        print(person["name"] + ": 肥満気味")
