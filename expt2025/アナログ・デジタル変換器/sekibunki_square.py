# 積分器に矩形波を入力したときの応答
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
# 10 Hz
df_10Hz = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/data_square_10Hz.csv"),
    skiprows=24,
    header=0,
)
# 100 Hz
df_100Hz = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/data_square_100Hz.csv"),
    skiprows=24,
    header=0,
)

#### -------- グラフ設定 -------- ####
plt.rcParams["font.size"] = 12  # フォントサイズ設定
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["figure.figsize"] = (8, 6)  # グラフのサイズを設定

#### -------- データをプロット(グラフ1: low) -------- ####
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(
    df_10Hz["Time (s)"], df_10Hz["Channel 1 (V)"], linestyle="solid", lw=1, label="入力"
)
ax2 = ax1.twinx()
ax2.plot(
    df_10Hz["Time (s)"],
    df_10Hz["Channel 2 (V)"],
    linestyle="solid",
    lw=1,
    label="出力",
    color="red",
)

ax1.set_xlabel("時間(t)")
ax1.set_ylabel("入力電圧 (V)")
ax2.set_ylabel("出力電圧 (V)")
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
legend1 = ax2.legend(h1 + h2, l1 + l2, loc="lower right", framealpha=1)

#### -------- データをプロット(グラフ1: low) -------- ####
fig2, ax3 = plt.subplots(figsize=(8, 6))
ax3.plot(
    df_100Hz["Time (s)"],
    df_100Hz["Channel 1 (V)"],
    linestyle="solid",
    lw=1,
    label="入力",
)
ax4 = ax3.twinx()
ax4.plot(
    df_100Hz["Time (s)"],
    df_100Hz["Channel 2 (V)"],
    linestyle="solid",
    lw=1,
    label="出力",
    color="red",
)

ax3.set_xlabel("時間(t)")
ax3.set_ylabel("入力電圧 (V)")
ax4.set_ylabel("出力電圧 (V)")
h3, l3 = ax3.get_legend_handles_labels()
h4, l4 = ax4.get_legend_handles_labels()
legend2 = ax4.legend(h3 + h4, l3 + l4, loc="lower right", framealpha=1)

#### -------- グラフを描画・保存 -------- ####
try:
    fig1.savefig("/home/jinaoyagi/pictures/20250619_実験/積分器_矩形波10Hz.png")
    fig2.savefig("/home/jinaoyagi/pictures/20250619_実験/積分器_矩形波100Hz.png")
    print("画像の保存が完了しました")
    # plt.show()
except Exception as e:
    print(f"エラー: {e}")
