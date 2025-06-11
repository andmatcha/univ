import numpy as np
import matplotlib.pyplot as plt


# 初期値リスト
intervals = [(5.0, -5.0), (5.0, 0.0), (1.0, 0.0), (2.0, 1.0)]


# 関数
def f(x):
    return np.exp(-x) - x**2


# 二分法
def bisection_method(f, a, b, eps=5e-6):
    if f(a) * f(b) > 0:
        print(f"初期区間 [{a}, {b}] に解が存在しません")
        return None, []

    mids = []
    while abs(b - a) >= eps:
        c = (a + b) / 2
        mids.append(c)

        if f(c) == 0.0:
            break
        elif f(c) * f(a) < 0:
            b = c
        else:
            a = c

    return c, mids


# グラフ描画準備
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.figure(figsize=(10, 6))
colors = ["r", "g", "b", "purple"]

# 実行
for i, (a, b) in enumerate(intervals):
    result, mids = bisection_method(f, a, b)
    if result is not None:
        plt.plot(
            range(1, len(mids) + 1),
            mids,
            label=f"a={a}, b={b}（{len(mids)}回）",
            color=colors[i],
        )
        print(f"区間 [{a}, {b}] の解: {result:.7f}, 繰り返し回数: {len(mids)}")

# 真の解
true_root = 0.7034674
plt.axhline(true_root, color="black", linestyle="--", label="真の解")

# グラフ設定、描画
plt.xlabel("繰り返し回数")
plt.ylabel("中間値（c）")
plt.title("初期値による収束の様子（f(x) = exp(-x) - x^2）")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
