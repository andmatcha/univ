# 振幅特性(バターワース) 理想曲線を追加

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/1.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"]  # 振幅(Hz)
y = df["y"]  # 利得(dB)

# 定数
R = 620
L = 0.040
C = 47.0e-9

# 周波数fの範囲
# 100Hzから15000Hzまで500点
f = np.logspace(2, np.log10(15000), 500)

# |H(jω)| を計算する関数
def calculate_abs_H_jw(w, R_val, L_val, C_val):
    X_w = 2 * R_val * (1 - w**2 * L_val * C_val)
    Y_w_term1 = L_val + 2 * C_val * R_val**2
    Y_w_term2 = w**2 * L_val * C_val**2 * R_val**2
    Y_w = w * (Y_w_term1 - Y_w_term2)

    abs_H = R_val / np.sqrt(X_w**2 + Y_w**2)
    return abs_H


# 各ωで|H(jω)|を計算
abs_H_values = calculate_abs_H_jw(2 * np.pi * f, R, L, C)

# デシベルに変換
gain_dB = 20 * np.log10(abs_H_values)


# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("振幅(Hz)")
plt.ylabel("利得(dB)")

# グラフを描画
plt.plot(f, gain_dB, label="理論値")
plt.plot(x, y, "ko", linestyle="solid", lw=1, markersize=3, label="実験値")
plt.xscale("log")
plt.legend()
plt.show()
