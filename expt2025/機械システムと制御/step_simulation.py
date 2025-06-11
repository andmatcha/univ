# ステップ応答 シミュレーション case1

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/freq_simulation_case1.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"]  # 時間 (s)
y1 = df["y1"]  # 変位 (m)
y2 = df["y2"]  # 変位 (m)

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("時間 (s)", fontsize="12")
plt.ylabel("変位 (m)", fontsize="12")
plt.xticks(fontsize="12")
plt.yticks(fontsize="12")

# グラフを描画
plt.plot(x, y1, linestyle="dashed", color="blue", lw=1, label="入力")
plt.plot(x, y2, linestyle="solid", color="red", lw=1.4, label="出力")
plt.legend()
plt.show()
