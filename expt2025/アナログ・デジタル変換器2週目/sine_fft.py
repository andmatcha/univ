# 正弦波のFFTグラフ
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

#### -------- ファイル読み込み -------- ####
filenames = ["AC_400Hz_1sec_extracted_fft.csv", "AC_600Hz_1sec_extracted_fft.csv"]

data_dir = Path(__file__).resolve().parent.joinpath("data")
dataframes = {}
for filename in filenames:
    # 1. 辞書のキーを作成する
    filename_splitted = filename.split("_")
    key = filename_splitted[0]  + "_" + filename_splitted[1]

    # 2. ファイルのフルパスを作成する
    file_path = data_dir.joinpath(filename)

    # 3. CSVを読み込み、辞書に格納する
    if file_path.exists():
        dataframes[key] = pd.read_csv(file_path)
    else:
        print(f"警告: ファイルが見つかりません: {file_path}")

#### -------- グラフ設定 -------- ####
plt.rcParams["font.size"] = 12
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
    ax.plot(
        df["Frequency"],
        df["PSD"],
        linestyle="solid",
        lw=1,
    )

    # 3. ラベルとタイトルを設定
    ax.set_xlabel("周波数 (Hz)")
    ax.set_ylabel("パワースペクトル密度 (dB)")

    # 4. グラフをファイルとして保存
    save_path = output_dir.joinpath(f"{name}_plot.png")
    plt.savefig(save_path, dpi=300)

    # 5. メモリを解放するために、プロットを閉じる（重要）
    plt.close(fig)

print(f"\n✅️保存完了: すべてのグラフが '{output_dir}' に保存されました。")
