# ステップ応答 シミュレーション case1

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/omega_phase_falling.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
omega = df["omega"]  # 周波数
phase = df["phase"]  # 位相

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("角周波数 (rad/s)", fontsize="12")
plt.ylabel("位相 (deg)", fontsize="12")
plt.xticks(fontsize="12")
plt.yticks(fontsize="12")

# グラフを描画
plt.plot(omega, phase,"ko-", lw=1)
plt.show()
