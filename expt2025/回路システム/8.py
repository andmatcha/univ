import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
from pathlib import Path

# データ
# 注意: 以下のCSVファイルの'y'列は位相データ(度)であると仮定します。
#       x列: 周波数(Hz), y列: 位相(度)
#       もし実際の列名が異なる場合は、下の df["x"] や df["y"] の部分を修正してください。
data_path = Path(__file__).resolve().parent.joinpath("data/6.csv")
# CSVファイルの読み込み
try:
    df = pd.read_csv(data_path, header=0)
    # グラフ用に実験データを整理
    x_experimental_freq = df["x"]  # 周波数 (Hz)
    y_experimental_phase = df["y"]  # 位相 (度) - CSVのy列を位相データとして解釈
    experimental_data_available = True
except FileNotFoundError:
    print(
        f"警告: 実験データファイル {data_path} が見つかりませんでした。理論曲線のみ表示します。"
    )
    experimental_data_available = False
    x_experimental_freq = pd.Series(dtype=float)  # 空のSeries
    y_experimental_phase = pd.Series(dtype=float)  # 空のSeries
except KeyError:
    print(
        f"警告: CSVファイルに 'x' または 'y' の列が見つかりません。理論曲線のみ表示します。"
    )
    experimental_data_available = False
    x_experimental_freq = pd.Series(dtype=float)
    y_experimental_phase = pd.Series(dtype=float)


# グラフ設定
plt.rcParams["font.family"] = (
    "Hiragino Mincho ProN"  # ご利用の環境に合わせてフォント名を変更してください
)
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

# --- 定数設定 ---
Q_spec = 1.0
R = 10e3  # 10kΩ
R0 = 10e3  # 10kΩ
R1 = 100e3  # 100kΩ
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
# プロットする周波数範囲を決定
# 理論計算のf0を中心に、実験データの範囲も考慮
min_freq_plot_log = np.log10(f0_calc / 1000)
max_freq_plot_log = np.log10(f0_calc * 100)

if experimental_data_available and not x_experimental_freq.empty:
    if x_experimental_freq.min() > 0:  # log10 の引数は正である必要あり
        min_freq_plot_log = min(min_freq_plot_log, np.log10(x_experimental_freq.min()))
    if x_experimental_freq.max() > 0:
        max_freq_plot_log = max(max_freq_plot_log, np.log10(x_experimental_freq.max()))

# 周波数点が少なすぎる場合や範囲が狭すぎる場合の安全策
if max_freq_plot_log <= min_freq_plot_log:
    max_freq_plot_log = min_freq_plot_log + 6  # logスケールで6桁分 (例: 1Hz to 1MHz)

frequencies_hz_theoretical = np.logspace(
    min_freq_plot_log, max_freq_plot_log, num_points
)
angular_frequencies_rad_theoretical = 2 * np.pi * frequencies_hz_theoretical

w_rad_out, mag_db_theoretical, phase_deg_theoretical = signal.bode(
    lpf_system, w=angular_frequencies_rad_theoretical
)

# --- 位相特性グラフ描画 (実験データと理論曲線を重ねて表示) ---
fig_phase, ax_phase = plt.subplots(figsize=(9, 6))

# 1. CSVデータからのグラフを描画 (実験データ - 位相)
if experimental_data_available and not x_experimental_freq.empty:
    ax_phase.plot(
        x_experimental_freq /1000,
        y_experimental_phase,
        color="black",
        marker="o",
        linestyle="solid",  # データポイントのみ表示。線で結ぶ場合は "solid" など
        linewidth=1,
        markersize=5,
        label="実験値",
    )

# 2. 計算された伝達関数からのグラフを描画 (理論曲線 - 位相)
ax_phase.plot(
    frequencies_hz_theoretical/1000,
    phase_deg_theoretical -180,
    linestyle="solid",
    linewidth=1.5,
    label=f"理論値",
)

# グラフの装飾
ax_phase.set_xlabel("周波数 (kHz)")
ax_phase.set_ylabel("位相 (deg)")

ax_phase.set_xlim(0, 15.1)
ax_phase.set_ylim(-180, 10)

ax_phase.legend(fontsize=10)
plt.show()

# 導出された伝達関数 H(jω) の表示
print("\n--- 伝達関数 H(jω) ---")
K1_val_str = f"{K1:.5e}"
num_str = f"{-K2 * omega_i**2:.5e}"
den_const_str = f"{K3 * omega_i**2:.5e}"
den_omega_coeff_str = f"{K1 * omega_i:.5e}"

print(f"H(jω) = {num_str} / (({den_const_str} - ω^2) + j ({den_omega_coeff_str} * ω))")
print(f"ここで、ω は角周波数 (rad/s) です。")
