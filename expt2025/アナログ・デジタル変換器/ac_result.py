# シングルスロープADCにsin波を入力したときの応答
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
# AC low
df_low = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/AC_low_result.csv"),
    header=0,
)
# AC high
df_high = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/AC_high_result.csv"),
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
    np.linspace(0, 0.512, len(df_low)),
    df_low["V"],
    linestyle="solid",
    lw=1,
)

ax1.set_xlabel("時刻(s)")
ax1.set_ylabel("出力 (V)")

#### -------- データをプロット(グラフ2: high) -------- ####
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(
    np.linspace(0, 0.512, len(df_high)),
    df_high["V"],
    linestyle="solid",
    lw=1,
)

ax2.set_xlabel("時刻(s)")
ax2.set_ylabel("出力 (V)")

#### -------- グラフを描画・保存 -------- ####
try:
    fig1.savefig("/home/jinaoyagi/pictures/20250619_実験/sin波応答_low.png")
    fig2.savefig("/home/jinaoyagi/pictures/20250619_実験/sin波応答_high.png")
    print("画像の保存が完了しました")
    # plt.show()
except Exception as e:
    print(f"エラー: {e}")
