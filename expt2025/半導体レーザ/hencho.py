# 変調特性
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
filenames = [
    "3-3_1_100Hz.CSV",
    "3-3_2_250Hz.CSV",
    "3-3_3_500Hz.CSV",
    "3-3_4_1kHz.CSV",
    "3-3_5_10kHz.CSV",
    "3-3_6_25kHz.CSV",
    "3-3_7_100kHz.CSV",
    "3-3_8_250kHz.CSV",
    "3-3_9_500kHz.CSV",
]

data_dir = Path(__file__).resolve().parent.joinpath("data")
dataframes = {}
for filename in filenames:
    # 1. 辞書のキーを作成する
    key = filename.split("_")[2].split(".")[0]

    # 2. ファイルのフルパスを作成する
    file_path = data_dir.joinpath(filename)

    # 3. CSVを読み込み、辞書に格納する
    if file_path.exists():
        dataframes[key] = pd.read_csv(
            file_path,
            skiprows=15,
            header=0,
        )
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

# 1. 新しいグラフ領域(Figure)と描画領域(Axes)を作成
fig, ax = plt.subplots(nrows=9, ncols=1, figsize=(10, 24))
i = 0
for name, df in dataframes.items():
    print(f"グラフを作成中: {name}")
    # 2. データをプロット
    t = df["TIME"]
    v = df["CH1"]

    ax[i].plot(t, v, linestyle="solid", lw=1, label=name)

    # 3. ラベルとタイトルを設定
    ax[i].set_title(name)
    ax[i].set_xlabel("時間 (s)")
    ax[i].set_ylabel("電圧 (V)")

    i += 1

plt.tight_layout()

# 4. グラフをファイルとして保存
save_path = output_dir.joinpath("3-3_plot.png")
plt.savefig(save_path, dpi=300)

# 5. メモリを解放するために、プロットを閉じる（重要）
plt.close(fig)

print(f"\n✅️保存完了: すべてのグラフが '{output_dir}' に保存されました。")
