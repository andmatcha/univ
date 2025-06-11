import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/6.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"]  # 電流
y = df["y"]  # 光出力

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("電流 (mA)")
plt.ylabel("光出力 (μW)")

# グラフを描画
plt.plot(x, y, "ko", linestyle="solid", lw=1, markersize=3)
plt.show()
