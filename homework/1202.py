import random

# 二分探索
def binary_search(data, key):
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        if data[mid] == key:
            return mid
        elif data[mid] < key:
            left = mid + 1
        else:
            right = mid - 1

    return -1

# 配列を生成
n = random.randint(10, 20)
random_array = [
    random.randint(1, 100) for _ in range(n)
]

# 配列をソート
random_array.sort()

try:
    target = int(input("探したい値を入力してください: "))
except ValueError:
    print("整数を入力してください")
    exit()

# 二分探索を実行
index = binary_search(random_array, target)

# 結果を表示
if index != -1:
    print(f"値 {target} は配列のインデックス {index} に存在します。")
else:
    print(f"値 {target} は配列内に存在しません。")
