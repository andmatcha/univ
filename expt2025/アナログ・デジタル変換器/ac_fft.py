# シングルスロープADCにsin波を入力したときの応答
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

#### -------- 定数 -------- ####
FREQ_LOW = 9.765625
FREQ_HIGH = 197.265625

#### -------- ファイル読み込み -------- ####
# AC low
df_low = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/AC_low_fft.csv"),
    header=0,
)
# AC high
df_high = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/AC_high_fft.csv"),
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
    df_low["Frequency"],
    df_low["Magnitude"],
    linestyle="solid",
    lw=1,
)

ax1.set_xlabel("周波数(Hz)")
ax1.set_ylabel("振幅 (dB)")

# ax1.axvline(FREQ_LOW, 0, 1, color="r", linestyle="dashed", lw="1") # 基本波

#### -------- データをプロット(グラフ2: high) -------- ####
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(
    df_high["Frequency"],
    df_high["Magnitude"],
    linestyle="solid",
    lw=1,
)

ax2.set_xlabel("周波数(Hz)")
ax2.set_ylabel("振幅 (dB)")

# ax2.axvline(FREQ_HIGH, 0, 1, color="r", linestyle="dashed", lw="1") # 基本波

#### -------- グラフを描画・保存 -------- ####
try:
    fig1.savefig("/home/jinaoyagi/pictures/20250619_実験/sin波fft_low.png")
    fig2.savefig("/home/jinaoyagi/pictures/20250619_実験/sin波fft_high.png")
    print("画像の保存が完了しました")
    # plt.show()
except Exception as e:
    print(f"エラー: {e}")
