# 発光フィールドのグラフ
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
filenames = [
    "x_power.csv",
    "y_power.csv",
]

data_dir = Path(__file__).resolve().parent.joinpath("data")
dataframes = {}
for filename in filenames:
    # 1. 辞書のキーを作成する
    key = filename.split("_")[0]

    # 2. ファイルのフルパスを作成する
    file_path = data_dir.joinpath(filename)

    # 3. CSVを読み込み、辞書に格納する
    if file_path.exists():
        dataframes[key] = pd.read_csv(file_path)
    else:
        print(f"警告: ファイルが見つかりません: {file_path}")

#### -------- グラフ設定 -------- ####
plt.rcParams["font.size"] = 14
plt.rcParams["font.family"] = "Noto Sans JP"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

#### -------- データをプロット -------- ####
output_dir = Path(__file__).resolve().parent.joinpath("figures")
output_dir.mkdir(exist_ok=True)
for name, df in dataframes.items():
    print(f"グラフを作成中: {name}")

    # 1. 新しいグラフ領域(Figure)と描画領域(Axes)を作成
    fig, ax = plt.subplots(figsize=(8, 6))

    # 2. データをプロット
    d = df["distance (mm)"]
    p = df["power (uW)"]
    peak_p = df.loc[p.idxmax(), "power (uW)"]
    peak_d = df.loc[p.idxmax(), "distance (mm)"]
    cutoff = peak_p / (np.e**2)

    ax.plot(
        d - peak_d,
        p,
        linestyle="solid",
        lw=1,
    )
    ax.axhline(cutoff, 0, 1, color="r", linestyle="dashed", lw="1")

    # 交点の近似点を求める
    exact_matches = df[df["power (uW)"] == cutoff]
    intersection_x_values = exact_matches["distance (mm)"].tolist()
    relative_pos = np.sign(df["power (uW)"] - cutoff)
    crossing_points_mask = relative_pos.diff().fillna(0).ne(0)
    crossing_indices = df.index[crossing_points_mask & (df["power (uW)"] != cutoff)]
    for idx in crossing_indices:
        # 注目点 (x2, y2)
        p2 = df.loc[idx]
        x2, y2 = p2["distance (mm)"], p2["power (uW)"]

        # 1つ前の点 (x1, y1)
        p1 = df.loc[idx - 1]
        x1, y1 = p1["distance (mm)"], p1["power (uW)"]

        # 線形補間の公式
        # x = x1 + (x2 - x1) * (target_y - y1) / (y2 - y1)
        if (y2 - y1) != 0:  # ゼロ除算を避ける
            x_intersect = x1 + (x2 - x1) * (cutoff - y1) / (y2 - y1)
            intersection_x_values.append(x_intersect)
    intersection_x_values.sort()
    omega = np.abs((intersection_x_values[1] - intersection_x_values[0]) / 2)
    print(f"スポット径: {omega:4f}")


    # 3. ラベルとタイトルを設定
    ax.set_xlabel("変位 (mm)")
    ax.set_ylabel("光パワ ($\mu$W)")

    # 4. グラフをファイルとして保存
    save_path = output_dir.joinpath(f"{name}_plot.png")
    plt.savefig(save_path, dpi=300)

    # 5. メモリを解放するために、プロットを閉じる（重要）
    plt.close(fig)

print(f"\n✅️保存完了: すべてのグラフが '{output_dir}' に保存されました。")
