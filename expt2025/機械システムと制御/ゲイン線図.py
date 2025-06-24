# ステップ応答 シミュレーション case1

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# 定数
xi = 0.707
omega_n = 4.0
w = np.logspace(-1, 1)
G_dB = -20 * np.log10(
    np.sqrt((1 - (w / omega_n) ** 2) ** 2 + (2 * xi * w / omega_n) ** 2)
)


# データ
data_path = Path(__file__).resolve().parent.joinpath("data/omega_gain_analysis.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
omega = df["omega"] / omega_n  # 周波数
gain = df["gain"]  # ゲイン

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("$ω/ω_{n}$", fontsize="12")
plt.ylabel("ゲイン (dB)", fontsize="12")
plt.xticks(fontsize="12")
plt.yticks(fontsize="12")
plt.xscale("log")

# グラフを描画
plt.plot(omega, gain, "ko-", lw=1, label="実験値")
plt.plot(w, G_dB, "b-", lw=1, label="制御モデル")
plt.legend()
plt.show()
