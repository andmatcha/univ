# 振幅特性(RC回路)

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/5.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
x = df["x"]  # 振幅(Hz)
y = df["y"]  # 利得(dB)

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("振幅(Hz)")
plt.ylabel("利得(dB)")

# グラフを描画
plt.plot(x, y, "ko", linestyle="solid", lw=1, markersize=3)
plt.xscale("log")
plt.show()
