import random

data = random.sample(range(1, 100), 20)

print("ソート前")
print(data)

for i in range(len(data)):
    max = i
    for j in range(i + 1, len(data)):
        if data[max] < data[j]:
            max = j

    data[i], data[max] = data[max], data[i]

print("ソート後")
print(data)
