import numpy as np
import matplotlib.pyplot as plt

# 定数 (以前の例の値を使用)
R = 620.0  # Ω
L = 0.040  # H (40mH)
C = 47.0e-9  # F (47nF)

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

# グラフ描画
plt.figure(figsize=(10, 6))
plt.plot(frequency_hz /1000, phase_values_deg_unwrapped)
plt.xlabel("Frequency f (kHz)")
plt.ylabel("Phase [degrees]")
plt.title("Unwrapped Phase Response of the LC Filter")
plt.grid(True, which="both", ls="-")
# y軸の目盛りを調整したい場合は、必要に応じて以下のコメントを解除・調整してください
# min_phase = np.min(phase_values_deg_unwrapped)
# max_phase = np.max(phase_values_deg_unwrapped)
# plt.yticks(np.arange(np.floor(min_phase / 45) * 45, np.ceil(max_phase / 45) * 45 + 45, 45))
plt.show()
