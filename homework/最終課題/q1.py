import random

data_asc = range(1000)
data_desc = range(999, -1, -1)
data_rand_list = [random.sample(range(1000), 1000) for _ in range(10)]


# 単純挿入法
def insertion_sort(data):
    data = list(data)
    comparisons = 0  # 比較回数
    swaps = 0  # 交換回数
    for i in range(1, len(data)):
        tmp = data[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if data[j] > tmp:
                data[j + 1] = data[j]
                swaps += 1
            else:
                break
            j -= 1
        data[j + 1] = tmp
    return data, comparisons, swaps


# 単純交換法
def bubble_sort(data):
    data = list(data)
    comparisons = 0  # 比較回数
    swaps = 0  # 交換回数
    for i in range(len(data)):
        for j in range(len(data) - i - 1):
            comparisons += 1
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swaps += 1
    return data, comparisons, swaps


# クイックソート
def quick_sort(data):
    data = list(data)
    comparisons = 0  # 比較回数
    swaps = 0  # 交換回数

    def _quick_sort(data, left, right):
        nonlocal comparisons, swaps
        if left >= right:
            return
        pivot = data[(left + right) // 2]
        i, j = left, right
        while True:
            while data[i] < pivot:
                comparisons += 1
                i += 1
            comparisons += 1
            while pivot < data[j]:
                comparisons += 1
                j -= 1
            comparisons += 1
            if i >= j:
                comparisons += 1
                break
            comparisons += 1
            data[i], data[j] = data[j], data[i]
            swaps += 1
            i += 1
            j -= 1
        _quick_sort(data, left, i - 1)
        _quick_sort(data, j + 1, right)

    _quick_sort(data, 0, len(data) - 1)
    return data, comparisons, swaps


def avg(list):
    return sum(list) / len(list)


# ソートを実行
result = {}
result["insertion_sort"] = {
    "asc": insertion_sort(data_asc),
    "desc": insertion_sort(data_desc),
    "rand": list(map(insertion_sort, data_rand_list)),
}
result["bubble_sort"] = {
    "asc": bubble_sort(data_asc),
    "desc": bubble_sort(data_desc),
    "rand": list(map(bubble_sort, data_rand_list)),
}
result["quick_sort"] = {
    "asc": quick_sort(data_asc),
    "desc": quick_sort(data_desc),
    "rand": list(map(quick_sort, data_rand_list)),
}


# 結果を表示
print("--------比較回数--------")
print(
    f"[単純挿入法] 昇順: {result['insertion_sort']['asc'][1]}, 降順: {result['insertion_sort']['desc'][1]}, 乱数: {avg(list(map(lambda x: x[1], result['insertion_sort']['rand'])))}"
)
print(
    f"[単純交換法] 昇順: {result['bubble_sort']['asc'][1]}, 降順: {result['bubble_sort']['desc'][1]}, 乱数: {avg(list(map(lambda x: x[1], result['bubble_sort']['rand'])))}"
)
print(
    f"[クイックソート] 昇順: {result['quick_sort']['asc'][1]}, 降順: {result['quick_sort']['desc'][1]}, 乱数: {avg(list(map(lambda x: x[1], result['quick_sort']['rand'])))}"
)


print("--------交換回数--------")
print(
    f"[単純挿入法] 昇順: {result['insertion_sort']['asc'][2]}, 降順: {result['insertion_sort']['desc'][2]}, 乱数: {avg(list(map(lambda x: x[2], result['insertion_sort']['rand'])))}"
)
print(
    f"[単純交換法] 昇順: {result['bubble_sort']['asc'][2]}, 降順: {result['bubble_sort']['desc'][2]}, 乱数: {avg(list(map(lambda x: x[2], result['bubble_sort']['rand'])))}"
)
print(
    f"[クイックソート] 昇順: {result['quick_sort']['asc'][2]}, 降順: {result['quick_sort']['desc'][2]}, 乱数: {avg(list(map(lambda x: x[2], result['quick_sort']['rand'])))}"
)
