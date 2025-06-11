import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/1.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0, index_col=0)

# グラフ用にデータを整理
# v = df["V"]
c1 = df["C1"]
c2 = df["C2"].dropna(how="any")

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("電圧(V)")
plt.ylabel("容量(pF)")
plt.xticks(range(-16, 17))

# グラフを描画
plt.plot(c1, "ko", linestyle="solid", lw=1, markersize=3, color="b", label="電圧増加方向")
plt.plot(c2, "ko", linestyle="solid", lw=1, markersize=3, color="g", label="電圧減少方向")

plt.legend(labels=["電圧増加方向", "電圧減少方向"])
plt.show()
plt.savefig("300_dpi_scatter.png", format="png", dpi=300)
