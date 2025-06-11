# 効率化した開き直り数の探索

import time
from itertools import combinations_with_replacement

# べき乗の値を事前に計算しておく
power_values = {d: d**d if d != 0 else 0 for d in range(10)}


# 指定範囲内の開き直り数を探索
def find_h_numbers(start, end):
    results = []
    count = 0
    # 各桁の数字の組み合わせを生成して判定
    for num_digits in range(len(str(start)), len(str(end)) + 1):
        for comb in combinations_with_replacement(range(10), num_digits):
            total = sum(power_values[d] for d in comb)
            count += 1
            if start <= total <= end and sorted(comb) == sorted(map(int, str(total))):
                results.append(total)
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
