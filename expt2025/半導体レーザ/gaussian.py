import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

df_x = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/x_power.csv"),
    header=0,
)
df_y = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/y_power.csv"),
    header=0,
)

# 1. ガウシアンモデル関数を定義
#    x: 位置データ
#    I0, x0, w, C: フィッティングするパラメータ
def gaussian(x, I0, x0, w, C):
    return I0 * np.exp(-2 * ((x - x0) / w) ** 2) + C


# 2. 実験データ
# x方向
x_data = df_x["distance (mm)"]
x_data_intensity = df_x["power (uW)"]
# y方向
y_data = df_y["distance (mm)"]
y_data_intensity = df_y["power (uW)"]


# 3. フィッティングの実行 (x方向)
# パラメータの初期値の推定（省略可能だが、与えると安定しやすい）
initial_guess_x = [
    max(x_data_intensity),
    x_data[np.argmax(x_data_intensity)],
    1,
    min(x_data_intensity),
]
# curve_fitでフィッティング
# popt: 最適化されたパラメータ [I0, x0, w, C]
# pcov: パラメータの共分散行列
popt_x, pcov_x = curve_fit(gaussian, x_data, x_data_intensity, p0=initial_guess_x)

# 4. 結果の取得と表示 (x方向)
I0_fit_x, x0_fit_x, wx_fit, C_fit_x = popt_x
spot_diameter_x = 2 * wx_fit

print("--- X-direction Fitting Results ---")
print(f"Peak Intensity (I0): {I0_fit_x:.2f}")
print(f"Center Position (x0): {x0_fit_x:.2f} mm")
print(f"Spot Radius (w_x): {wx_fit:.4f} mm")
print(f"Baseline Offset (C): {C_fit_x:.2f}")
print(f"Spot Diameter (D_x = 2*w_x): {spot_diameter_x:.4f} mm")
print("-----------------------------------")


# 5. フィッティングの実行 (y方向)
initial_guess_y = [
    max(y_data_intensity),
    y_data[np.argmax(y_data_intensity)],
    1,
    min(y_data_intensity),
]
popt_y, pcov_y = curve_fit(gaussian, y_data, y_data_intensity, p0=initial_guess_y)

# 6. 結果の取得と表示 (y方向)
I0_fit_y, y0_fit_y, wy_fit, C_fit_y = popt_y
spot_diameter_y = 2 * wy_fit

print("\n--- Y-direction Fitting Results ---")
print(f"Peak Intensity (I0): {I0_fit_y:.2f}")
print(f"Center Position (y0): {y0_fit_y:.2f} mm")
print(f"Spot Radius (w_y): {wy_fit:.4f} mm")
print(f"Baseline Offset (C): {C_fit_y:.2f}")
print(f"Spot Diameter (D_y = 2*w_y): {spot_diameter_y:.4f} mm")
print("-----------------------------------")


# 7. グラフ
plt.rcParams["font.size"] = 14
plt.rcParams["font.family"] = "Noto Sans JP"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"


# x方向のプロット
d_x = df_x["distance (mm)"]
p_x = df_x["power (uW)"]
peak_p_x = df_x.loc[p_x.idxmax(), "power (uW)"]
peak_d_x = df_x.loc[p_x.idxmax(), "distance (mm)"]
cutoff_x = peak_p_x / (np.e**2)

fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.scatter(x_data - peak_d_x, x_data_intensity, label="実験値", s=10)
ax1.plot(
    x_data - peak_d_x,
    gaussian(x_data, *popt_x),
    "k-",
    label=f"近似曲線",
)

ax1.axhline(cutoff_x, 0, 1, color="r", linestyle="dashed", lw="1")

ax1.set_xlabel("変位 (mm)")
ax1.set_ylabel("光パワ ($\mu$W)")
ax1.legend(loc="upper right", fontsize=12)

# y方向のプロット
d_y = df_y["distance (mm)"]
p_y = df_y["power (uW)"]
peak_p_y = df_y.loc[p_y.idxmax(), "power (uW)"]
peak_d_y = df_y.loc[p_y.idxmax(), "distance (mm)"]
cutoff_y = peak_p_y / (np.e**2)

fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.scatter(y_data - peak_d_y, y_data_intensity, label="実験値", s=10)
ax2.plot(
    y_data - peak_d_y,
    gaussian(y_data, *popt_y),
    "k-",
    label=f"近似曲線",
)

ax2.axhline(cutoff_x, 0, 1, color="r", linestyle="dashed", lw="1")

ax2.set_xlabel("変位 (mm)")
ax2.set_ylabel("光パワ ($\mu$W)")
ax2.legend(loc="upper right", fontsize=12)

# グラフをファイルとして保存
output_dir = Path(__file__).resolve().parent.joinpath("figures")
output_dir.mkdir(exist_ok=True)
save_path1 = output_dir.joinpath("x_gaussian_plot.png")
save_path2 = output_dir.joinpath("y_gaussian_plot.png")
fig1.savefig(save_path1, dpi=300)
fig2.savefig(save_path2, dpi=300)
# メモリを解放するために、プロットを閉じる（重要）
plt.close(fig1)
plt.close(fig2)

print(f"\n✅️保存完了: すべてのグラフが '{output_dir}' に保存されました。")
