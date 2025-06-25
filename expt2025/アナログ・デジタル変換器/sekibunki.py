# 積分器のゲインと位相
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
# 条件A 実験値
df_a = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_a.csv"),
    skiprows=25,
    header=0,
)
# 条件B 実験値
df_b = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_b.csv"),
    skiprows=25,
    header=0,
)
# 条件C 実験値
df_c = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_c.csv"),
    skiprows=25,
    header=0,
)
# ゲイン理論値
df_theoretical_gain = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_theoretical_gain.csv"),
    skiprows=1,
    header=0,
)
# 位相理論値
df_theoretical_phase = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_theoretical_phase.csv"),
    skiprows=1,
    header=0,
)

#### -------- グラフ設定 -------- ####
plt.rcParams["font.size"] = 12  # フォントサイズ設定
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"
plt.rcParams["figure.figsize"] = (8, 6)  # グラフのサイズを設定

#### -------- データをプロット(グラフ1: 積分器のゲイン特性 - 理論値) -------- ####
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(
    df_theoretical_gain["f"],
    df_theoretical_gain["Gain A"],
    label="条件A",
    linestyle="solid",
    color="red",
    lw=1,
)
ax1.plot(
    df_theoretical_gain["f"],
    df_theoretical_gain["Gain B"],
    label="条件B",
    linestyle="solid",
    color="green",
    lw=1,
)
ax1.plot(
    df_theoretical_gain["f"],
    df_theoretical_gain["Gain C"],
    label="条件C",
    linestyle="solid",
    color="blue",
    lw=1,
)
ax1.set_xscale("log")
ax1.set_xlabel("周波数 (Hz)")
ax1.set_ylabel("ゲイン (dB)")
ax1.legend()

#### -------- データをプロット(グラフ2: 積分器のゲイン特性 - 実験値) -------- ####
fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(
    df_a["Frequency (Hz)"],
    df_a["Channel 2 Magnitude (dB)"],
    label="条件A",
    linestyle="solid",
    color="red",
    lw=1,
)
ax2.plot(
    df_b["Frequency (Hz)"],
    df_b["Channel 2 Magnitude (dB)"],
    label="条件B",
    linestyle="solid",
    color="green",
    lw=1,
)
ax2.plot(
    df_c["Frequency (Hz)"],
    df_c["Channel 2 Magnitude (dB)"],
    label="条件C",
    linestyle="solid",
    color="blue",
    lw=1,
)
ax2.set_xscale("log")
ax2.set_xlabel("周波数 (Hz)")
ax2.set_ylabel("ゲイン (dB)")
ax2.legend()

#### -------- データをプロット(グラフ3: 積分器の位相特性 - 理論値) -------- ####
fig3, ax3 = plt.subplots(figsize=(8, 6))
ax3.plot(
    df_theoretical_phase["f"],
    df_theoretical_phase["Phase A"],
    label="条件A",
    linestyle="solid",
    color="red",
    lw=1,
)
ax3.plot(
    df_theoretical_phase["f"],
    df_theoretical_phase["Phase B"],
    label="条件B",
    linestyle="solid",
    color="green",
    lw=1,
)
ax3.plot(
    df_theoretical_phase["f"],
    df_theoretical_phase["Phase C"],
    label="条件C",
    linestyle="solid",
    color="blue",
    lw=1,
)
ax3.set_xscale("log")
ax3.set_xlabel("周波数 (Hz)")
ax3.set_ylabel("位相 (deg)")
ax3.legend()

#### -------- データをプロット(グラフ4: 積分器の位相特性 - 実験値) -------- ####
fig4, ax4 = plt.subplots(figsize=(8, 6))
ax4.plot(
    df_a["Frequency (Hz)"],
    df_a["Channel 2 Phase (deg)"],
    label="条件A",
    linestyle="solid",
    color="red",
    lw=1,
)
ax4.plot(
    df_b["Frequency (Hz)"],
    df_b["Channel 2 Phase (deg)"],
    label="条件B",
    linestyle="solid",
    color="green",
    lw=1,
)
ax4.plot(
    df_c["Frequency (Hz)"],
    df_c["Channel 2 Phase (deg)"],
    label="条件C",
    linestyle="solid",
    color="blue",
    lw=1,
)
ax4.set_xscale("log")
ax4.set_xlabel("周波数 (Hz)")
ax4.set_ylabel("位相 (deg)")
ax4.legend()

#### -------- グラフを描画・保存 -------- ####
try:
    fig1.savefig("/home/jinaoyagi/pictures/20250619_実験/積分器のゲイン特性(理論値).png")
    fig2.savefig("/home/jinaoyagi/pictures/20250619_実験/積分器のゲイン特性(実験値).png")
    fig3.savefig("/home/jinaoyagi/pictures/20250619_実験/積分器の位相特性(理論値).png")
    fig4.savefig("/home/jinaoyagi/pictures/20250619_実験/積分器の位相特性(実験値).png")
    print("画像の保存が完了しました")
except Exception as e:
    print(f"エラー: {e}")
