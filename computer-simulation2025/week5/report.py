import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Hiragino Mincho ProN"

# 初期条件と設定
N = 10  # 繰り返し回数
h = 0.1  # 数値微分の差分幅
ans = 0.8320389691517  # 真値
iterations = np.arange(1, N + 1)


# 関数f(x)
def f(x):
    """f(x) = tan^{-1}(x-1) + 0.2x"""
    return np.arctan(x - 1) + 0.2 * x


# 導関数df(x)
def df(x):
    """f'(x) = 1 / (1 + (x-1)^2) + 0.2"""
    return 1.0 / (1.0 + (x - 1) ** 2) + 0.2


# グラフ描画
def plot(errors, label, color):
    # グラフの描画
    plt.plot(iterations, errors, marker="o", linestyle="-", color=color, label=label)


# グラフ設定
def setup_graph():
    # y軸を対数スケールに設定
    plt.yscale("log")
    # タイトルとラベル
    plt.title("収束誤差の推移", fontsize=16)
    plt.xlabel("繰り返し回数 k", fontsize=12)
    plt.ylabel("絶対誤差 |ans - ${c_k}$|", fontsize=12)
    plt.xticks(iterations)
    plt.grid(True, which="both", linestyle="--")
    plt.legend()


# 二分法
def bisection(a, b):
    errors = []
    fa = f(a)
    for i in range(N):
        c = (a + b) / 2
        # 誤差の計算とリストへの保存
        error = np.abs(ans - c)
        errors.append(error)

        # 区間の更新
        if fa * f(c) < 0:
            b = c
        else:
            a = c
            fa = f(a)
    plot(errors, "二分法", "red")


# 導関数を用いたニュートン法
def newton_derivative(x_0):
    errors = []
    x_k = x_0
    for i in range(N):
        # 現在のx_kでの関数値と微分係数を計算
        fx = f(x_k)
        dfx = df(x_k)

        # 誤差の計算とリストへの保存
        error = np.abs(ans - x_k)
        errors.append(error)
        x_k = x_k - fx / dfx
    plot(errors, "導関数を用いたニュートン法", "blue")


# 数値微分を用いたニュートン法(差分幅0.1)
def newton_numerical(x_0):
    errors = []
    x_k = x_0
    for i in range(N):
        # 現在のx_kでの関数値を計算
        fx = f(x_k)

        # f'(x_k) を中心差分で近似計算
        # f'(x_k) ≈ (f(x_k + h) - f(x_k - h)) / (2 * h)
        dfx_approx = (f(x_k + h) - f(x_k - h)) / (2 * h)

        # 誤差の計算とリストへの保存
        error = np.abs(ans - x_k)
        errors.append(error)
        # 0除算回避
        if abs(dfx_approx) < 1e-15:
            break

        x_k = x_k - fx / dfx_approx
    plot(errors, "数値微分を用いたニュートン法", "green")


# 実行
bisection(0.0, 5.0)
newton_derivative(2.5)

# グラフ設定
plt.yscale("log")
plt.title("収束誤差の推移", fontsize=16)
plt.xlabel("繰り返し回数 k", fontsize=12)
plt.ylabel("絶対誤差 |ans - ${c_k}$|", fontsize=12)
plt.xticks(iterations)
plt.grid(True, which="both", linestyle="--")
plt.legend()

# グラフ描画
plt.show()
