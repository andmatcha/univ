# 総当たり法による開き直り数の探索

import time

# べき乗の値を事前に計算しておく
power_values = {d: d**d if d != 0 else 0 for d in range(10)}


# 開き直り数かどうかを判定
def is_h_number(num):
    digits = list(map(int, str(num)))
    total = sum(power_values[d] for d in digits)
    return total == num


# 指定範囲内の開き直り数を探索
def find_h_numbers(start, end):
    count = 0
    results = []
    for num in range(start, end + 1):
        if is_h_number(num):
            results.append(num)
        count += 1
    print("探索回数:", count)
    return results


# 探索範囲を指定
start = 1
end = 9999999999

# 探索を実行
time_start = time.perf_counter()  # 計測開始
h_numbers = find_h_numbers(start, end)  # 開き直り数を探索
time_end = time.perf_counter()  # 計測終了

# 結果を表示
print("開き直り数:", h_numbers)
print("実行時間:{:.4f}s".format((time_end - time_start)))
