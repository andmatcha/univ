# 位相特性(バターワース)

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/4.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"] / 1000  # 振幅(kHz)
y = df["y"]  # 位相(deg)


# 定数
R = 620
L = 0.020
C = 100.0e-9

# 周波数 f の範囲 (Hz単位、対数スケールで生成)
# 例えば 1 Hz から 1 MHz まで500点 (実験に合わせて調整してください)
frequency_hz = np.linspace(100, 15000, 500)
omega = 2 * np.pi * frequency_hz


# H(jω) の分母の実部と虚部を計算する関数
def calculate_denominator_parts(w, R_val, L_val, C_val):
    X_w = 2 * R_val * (1 - w**2 * L_val * C_val)

    Y_w_term1 = L_val + 2 * C_val * R_val**2
    Y_w_term2 = w**2 * L_val * C_val**2 * R_val**2
    Y_w = w * (Y_w_term1 - Y_w_term2)

    return X_w, Y_w


# 偏角を計算する関数 (出力は度単位、アンラップ処理を含む)
def calculate_phase_degrees_unwrapped(X_w, Y_w):
    # arctan2 で -π から π の範囲の角度（ラジアン）を計算
    phase_rad_wrapped = -np.arctan2(Y_w, X_w)

    # 位相をアンラップ（不連続なジャンプを補正）
    # np.unwrap はラジアン単位で処理するので、度への変換前に行う
    phase_rad_unwrapped = np.unwrap(phase_rad_wrapped)

    # ラジアンから度に変換
    phase_deg_unwrapped = np.degrees(phase_rad_unwrapped)
    return phase_deg_unwrapped


# 各ωで分母の実部と虚部を計算
X_omega, Y_omega = calculate_denominator_parts(omega, R, L, C)

# 各ωでアンラップされた偏角を計算 (度単位)
phase_values_deg_unwrapped = calculate_phase_degrees_unwrapped(X_omega, Y_omega)

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("振幅(kHz)")
plt.ylabel("位相(deg)")

# グラフを描画
plt.plot(frequency_hz / 1000, phase_values_deg_unwrapped, label="理論値")
plt.plot(x, y, "ko", linestyle="solid", lw=1, markersize=3, label="実験値")
plt.legend()
plt.show()
