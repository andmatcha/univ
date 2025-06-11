import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/1.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"]  # 波長
y = df["y"]  # 光電流

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("波長 (nm)")
plt.ylabel("光電流 (μA)")

# グラフを描画
plt.plot(x, y, "ko", linestyle="solid", lw=1, markersize=3)
plt.show()
