# 半導体レーザのしきい値を求める I-Pグラフ
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
df = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/i_th.csv"),
    header=0,
)

#### -------- グラフ設定 -------- ####
plt.rcParams["font.size"] = 14
plt.rcParams["font.family"] = "Noto Sans JP"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["figure.figsize"] = (8, 6)  # グラフのサイズを設定

#### -------- データをプロット -------- ####
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(
    df["I (mA)"],
    df["power (mW)"],
    linestyle="solid",
    lw=1,
    label="測定値"
)

ax.set_xlabel("注入電流 (mA)")
ax.set_ylabel("光パワ (mW)")

# 近似直線
a = 0.1092806786
b = -2.925320393
x = np.linspace(26.76887105, 40)
y = a * x + b
ax.plot(
    x,
    y,
    linestyle="dashed",
    lw=1,
    color="red",
    label="近似直線"
)

ax.legend()

#### -------- グラフを描画・保存 -------- ####
output_dir = Path(__file__).resolve().parent.joinpath("figures")
output_dir.mkdir(exist_ok=True)
filename = "I-P_plot.png"
save_path = output_dir.joinpath(filename)
try:
    plt.savefig(save_path, dpi=300)
    print(
        f"\n✅️保存完了: グラフは '{filename}' として '{output_dir}' に保存されました。"
    )
except Exception as e:
    print(f"エラー: {e}")
