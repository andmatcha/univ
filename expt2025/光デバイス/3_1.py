# 赤色LED(分光感度特性考慮)

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/3.csv")
data_path2 = Path(__file__).resolve().parent.joinpath("data/2.csv")  # 分光感度特性
# CSVファイルの読み込み
df1 = pd.read_csv(data_path, header=0)
df2 = pd.read_csv(data_path2, header=0)  # 分光感度特性
merged = pd.merge(df1, df2, on="x")

# グラフ用にデータを整理
x = merged["x"]  # 波長
y1 = merged["y1"] / merged["y"]  # 光電流 10mA
y2 = merged["y2"] / merged["y"]  # 光電流 20mA
y3 = merged["y3"] / merged["y"]  # 光電流 30mA

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
