# シングルスロープADCに矩形波を入力したときの応答
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
# 1 MHz
df_1MHz = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/Linear_1MHz_result.csv"),
    header=0,
)
# 500 kHz
df_500kHz = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/Linear_500kHz_result.csv"),
    header=0,
)
# 100 kHz
df_100kHz = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/Linear_100kHz_result.csv"),

    header=0,
)

#### -------- グラフ設定 -------- ####
plt.rcParams["font.size"] = 12  # フォントサイズ設定
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["figure.figsize"] = (8, 6)  # グラフのサイズを設定

#### -------- データをプロット(グラフ1: 1MHz) -------- ####
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(
    np.linspace(0, 0.5, len(df_1MHz)),
    df_1MHz["V"],
    linestyle="solid",
    lw=1,
)

ax1.set_xlabel("時刻(s)")
ax1.set_ylabel("出力 (V)")

#### -------- データをプロット(グラフ2: 500kHz) -------- ####
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(
    np.linspace(0, 0.5, len(df_500kHz)),
    df_500kHz["V"],
    linestyle="solid",
    lw=1,
)

ax2.set_xlabel("時刻(s)")
ax2.set_ylabel("出力 (V)")

#### -------- データをプロット(グラフ3: 100kHz) -------- ####
fig3, ax3 = plt.subplots(figsize=(8, 6))
ax3.plot(
    np.linspace(0, 0.5, len(df_100kHz)),
    df_100kHz["V"],
    linestyle="solid",
    lw=1,
)

ax3.set_xlabel("時刻(s)")
ax3.set_ylabel("出力 (V)")

#### -------- グラフを描画・保存 -------- ####
try:
    fig1.savefig("/home/jinaoyagi/pictures/20250619_実験/Ramp波応答_counter1MHz.png")
    fig2.savefig("/home/jinaoyagi/pictures/20250619_実験/Ramp波応答_counter500kHz.png")
    fig3.savefig("/home/jinaoyagi/pictures/20250619_実験/Ramp波応答_counter100kHz.png")
    print("画像の保存が完了しました")
    # plt.show()
except Exception as e:
    print(f"エラー: {e}")
