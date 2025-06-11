import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/8.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)

# グラフ用にデータを整理
# バイアスOFF
x = df["x"]  # 光入力 (μW)
y1 = df["y1"] * 1000  # 出力電圧 (mV) 1kΩ
y2 = df["y2"] * 1000  # 出力電圧 (mV) 10kΩ
y3 = df["y3"] * 1000  # 出力電圧 (mV) 100kΩ

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("光入力 (μW)")
plt.ylabel("出力電圧 (mV)")

# グラフを描画
plt.plot(x, y1, "ko", linestyle="solid", lw=1, markersize=3, color="r", label="1kΩ")
plt.plot(x, y2, "ko", linestyle="solid", lw=1, markersize=3, color="g", label="10kΩ")
plt.plot(x, y3, "ko", linestyle="solid", lw=1, markersize=3, color="b", label="100kΩ")
plt.legend(["1kΩ", "10kΩ", "100kΩ"])
plt.show()
