import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
from pathlib import Path

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/5.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x_experimental = df["x"]  # 周波数 (Hz) (元の"振幅(Hz)"から解釈変更)
y_experimental = df["y"]  # 利得 (dB)

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"  # ご利用の環境に合わせてフォント名を変更してください
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

# --- 定数設定 ---
Q_spec = 1.0
R = 10e3  # 10kΩ
R0 = 10e3  # 10kΩ
R1 = 100e3  # 100kΩ
# R3 = 100e3   # R3はK1の計算に直接使われない (Q指定のため)
# R4 = 40e3    # R4はK1の計算に直接使われない (Q指定のため)
R5 = 100e3  # 100kΩ
C = 1000e-12  # 1000pF = 1nF

# --- パラメータ計算 ---
K2 = R0 / R1
K3 = R0 / R5
K1 = np.sqrt(K3) / Q_spec
omega_i = 1 / (R * C)

# --- 伝達関数の係数 ---
numerator_coeffs = [-K2 * omega_i**2]
denominator_coeffs = [1, K1 * omega_i, K3 * omega_i**2]
lpf_system = signal.TransferFunction(numerator_coeffs, denominator_coeffs)

# --- 特性周波数とDCゲインの計算 (参考情報) ---
omega0_calc = omega_i * np.sqrt(K3)
f0_calc = omega0_calc / (2 * np.pi)
dc_gain_calc = -K2 / K3

print(f"--- 計算されたパラメータ ---")
print(f"K1 = {K1:.4f}")
print(f"K2 = {K2:.4f}")
print(f"K3 = {K3:.4f}")
print(f"ωi = {omega_i:.2e} rad/s")
print(f"自然角周波数 ω0 = {omega0_calc:.2f} rad/s")
print(f"自然周波数 f0 = {f0_calc:.2f} Hz")
print(f"DCゲイン H0 = {dc_gain_calc:.2f}")
print(f"指定されたQ値 = {Q_spec}")

# --- 周波数応答の計算 ---
num_points = 500
# プロットする周波数範囲を実験データの範囲も考慮して調整するとより良い場合があります
# ここでは理論計算のf0を中心に十分な範囲を取ります
min_freq_plot = min(x_experimental.min(), f0_calc / 1000) if not x_experimental.empty else f0_calc / 1000
max_freq_plot = max(x_experimental.max(), f0_calc * 100) if not x_experimental.empty else f0_calc * 100

# 周波数点が重複しないように、また対数的に均等になるように
# x_experimental の最小・最大値と f0_calc の周辺を考慮
# 簡単のため、元の理論値の周波数範囲設定を基本とします
frequencies_hz_theoretical = np.logspace(
    np.log10(f0_calc / 1000), np.log10(f0_calc * 100), num_points
)
angular_frequencies_rad_theoretical = 2 * np.pi * frequencies_hz_theoretical

w_rad_out, mag_db_theoretical, phase_deg_theoretical = signal.bode(
    lpf_system, w=angular_frequencies_rad_theoretical
)

# --- グラフ描画 (重ねて表示) ---
fig, ax = plt.subplots(figsize=(9, 6))

# 1. CSVデータからのグラフを描画 (実験データ)
# 元のプロット方法 (点と線) を踏襲し、semilogx を使用
ax.semilogx(
    x_experimental,
    y_experimental,
    color="black",
    marker="o",
    linestyle="solid",  # 点を線で結ぶ
    linewidth=1,
    markersize=3,
    label="実験値",
)

# 2. 計算された伝達関数からのグラフを描画 (理論曲線)
ax.semilogx(
    frequencies_hz_theoretical,
    mag_db_theoretical,
    linestyle="solid",
    linewidth=1.5, # 理論曲線の線幅を少し太くする
    label=f"理論値",
)

# グラフの装飾
ax.set_xlabel("周波数 (Hz)", fontsize="12") # X軸ラベルを「周波数 (Hz)」に変更
ax.set_ylabel("利得 (dB)", fontsize="12")

# Y軸の範囲を、実験データと理論曲線の両方が表示されるように調整
all_y_values = np.concatenate((y_experimental.values, mag_db_theoretical)) # y_experimentalがPandas Seriesのため .values を使用
min_y_val = all_y_values.min()
max_y_val = all_y_values.max()
ax.set_ylim(-20, max_y_val + 1)
ax.set_xlim(100 -10, 15000 + 1000)

ax.legend(fontsize=10, loc="upper right")  # 凡例を表示

plt.show()

# 導出された伝達関数 H(jω) の表示
print("\n--- 伝達関数 H(jω) ---")
K1_val_str = f"{K1:.5e}"
num_str = f"{-K2 * omega_i**2:.5e}"
den_const_str = f"{K3 * omega_i**2:.5e}"
den_omega_coeff_str = f"{K1 * omega_i:.5e}"

print(f"H(jω) = {num_str} / (({den_const_str} - ω^2) + j ({den_omega_coeff_str} * ω))")
print(f"ここで、ω は角周波数 (rad/s) です。")
