# 位相特性(チェビシェフ)

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/4.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"] / 1000  # 振幅(kHz)
y = df["y"]  # 位相(deg)

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("振幅(kHz)")
plt.ylabel("位相(deg)")

# グラフを描画
plt.plot(x, y, "ko", linestyle="solid", lw=1, markersize=3)
plt.show()
