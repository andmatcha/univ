# 赤色LED(実験値)

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/3.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"]  # 波長
y1 = df["y1"]  # 光電流 10mA
y2 = df["y2"]  # 光電流 20mA
y3 = df["y3"]  # 光電流 30mA

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("波長 (nm)")
plt.ylabel("光電流 (μA)")

# グラフを描画
plt.plot(x, y1, "ko", linestyle="solid", lw=1, markersize=3, color="r", label="10 mA")
plt.plot(x, y2, "ko", linestyle="solid", lw=1, markersize=3, color="g", label="20 mA")
plt.plot(x, y3, "ko", linestyle="solid", lw=1, markersize=3, color="b", label="30 mA")
plt.legend(["10 mA", "20 mA", "30 mA"])
plt.show()
