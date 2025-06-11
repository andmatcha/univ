# ステップ応答 シミュレーション case1

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

target_omega = 32

# データ
data_path = Path(__file__).resolve().parent.joinpath("data/freq_exp_all.csv")
# CSVファイルの読み込み
df = pd.read_csv(data_path, header=0)
df = df[df["omega"] == target_omega]

# グラフ用にデータを整理
t = df["t"]  # 時間 (s)
input = df["in"]  # 入力の変位 (m)
output = df["out"]  # 出力の変位 (m)

# グラフ設定
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

plt.xlabel("時間 (s)", fontsize="12")
plt.ylabel("変位 (m)", fontsize="12")
plt.xticks(fontsize="12")
plt.yticks(fontsize="12")

# グラフを描画
plt.plot(t, input, linestyle="dashed", color="blue", lw=1, label="入力")
plt.plot(t, output, linestyle="solid", color="red", lw=1.4, label="出力")
plt.legend()
plt.show()
