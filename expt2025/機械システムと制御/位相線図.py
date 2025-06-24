# ステップ応答 シミュレーション case1

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# 定数
xi = 0.2
omega_n = 4.0
w = np.logspace(-1, 1)
argG = np.rad2deg(-np.arctan2(2 * xi * (w / omega_n), 1 - (w / omega_n) ** 2))

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/omega_phase_falling.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
omega = df["omega"] / omega_n  # 周波数
phase = df["phase"]  # 位相

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("$ω/ω_{n}$", fontsize="12")
plt.ylabel("位相 (deg)", fontsize="12")
plt.xticks(fontsize="12")
plt.yticks(fontsize="12")
plt.xscale("log")

# グラフを描画
plt.plot(omega, phase, "ko-", lw=1, label="実験値")
plt.plot(w, argG, "b-", lw=1, label="制御モデル")
plt.legend()
plt.show()
