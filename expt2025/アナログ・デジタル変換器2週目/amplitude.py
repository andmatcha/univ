# 音楽データの振幅グラフ
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
filenames = [
    "newkawaii1_10MHz_10kHz_1sec_extracted.csv",
    "newkawaii2_400kHz_10kHz_1sec_extracted.csv",
    "newkawaii3_500kHz_500Hz_1sec_extracted.csv",
    "newkawaii4_20kHz_500Hz_1sec_extracted.csv"
    "waltz1_10MHz_10kHz_1sec_extracted.csv",
    "waltz2_400kHz_10kHz_1sec_extracted.csv",
    "waltz3_500kHz_500Hz_1sec_extracted.csv",
    "waltz4_20kHz_500Hz_1sec_extracted.csv",
    "BB1_10MHz_10kHz_1sec_extracted.csv",
    "BB2_400kHz_10kHz_1sec_extracted.csv",
    "BB3_500kHz_500Hz_1sec_extracted.csv",
    "BB4_20kHz_500Hz_1sec_extracted.csv",
]

data_dir = Path(__file__).resolve().parent.joinpath("data")
dataframes = {}
for filename in filenames:
    # 1. 辞書のキーを作成する
    #    例: "newkawaii1_..." -> "newkawaii1"
    key = filename.split("_")[0]

    # 2. ファイルのフルパスを作成する
    file_path = data_dir.joinpath(filename)

    # 3. CSVを読み込み、辞書に格納する
    if file_path.exists():
        dataframes[key] = pd.read_csv(file_path)
    else:
        print(f"警告: ファイルが見つかりません: {file_path}")

#### -------- グラフ設定 -------- ####
plt.rcParams["font.size"] = 12
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

#### -------- データをプロット -------- ####
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(
    dataframes["newkawaii1"]["Time"],
    dataframes["newkawaii1"]["Amplitude"],
    linestyle="solid",
    lw=1,
)
ax.set_xlabel("時刻(s)")
ax.set_ylabel("振幅")


output_dir = Path(__file__).resolve().parent.joinpath("figures")
output_dir.mkdir(exist_ok=True)
for name, df in dataframes.items():
    print(f"グラフを作成中: {name}")

    # 1. 新しいグラフ領域(Figure)と描画領域(Axes)を作成
    fig, ax = plt.subplots(figsize=(8, 6))

    # 2. データをプロット
    ax.plot(
        df["Time"],
        df["Amplitude"],
        linestyle="solid",
        lw=1,
    )

    # 3. ラベルとタイトルを設定
    ax.set_xlabel("時刻 (s)")
    ax.set_ylabel("振幅")

    # 4. グラフをファイルとして保存
    #    ファイル名は 'newkawaii1_plot.png' のようになります
    save_path = output_dir.joinpath(f"{name}_plot.png")
    plt.savefig(save_path)

    # 5. メモリを解放するために、プロットを閉じる（重要）
    plt.close(fig)

print(f"\n✅️保存完了: すべてのグラフが '{output_dir}' に保存されました。")
