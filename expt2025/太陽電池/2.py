import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import numpy as np


# --- グラフ描画・保存関数 ---
def plot_and_save_graph(
    data_path: Path, output_dir: Path, title_suffix: str = "", filename_prefix: str = ""
):
    """
    指定されたCSVファイルからデータを読み込み、グラフを画像として保存する関数。

    Args:
        data_path (Path): CSVファイルのパス。
        output_dir (Path): 画像の保存先ディレクトリ。
        title_suffix (str, optional): グラフタイトルに追加する接尾辞。デフォルトは空文字。
        filename_prefix (str, optional): 保存ファイル名の前につける接頭辞。デフォルトは空文字。
    """
    fig = plt.figure(figsize=(6, 4))  # サイズを指定して新しいFigureを作成
    plot_successful = False  # 初期ステータス
    try:
        # データが存在しない場合、画像保存せず終了
        if not data_path.exists():
            print(f"警告: ファイルが見つかりません: {data_path}")
            return

        # CSVファイルの読み込み
        df = pd.read_csv(data_path, header=0)

        # カラム存在チェック
        required_cols = ["V (V)", "I (mA)"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        # カラムに不足がある場合、画像保存せず終了
        if missing_cols:
            print(
                f"警告: {data_path.name} に必要なカラム {missing_cols} がありません。"
            )
            return

        # グラフ用にデータを整理
        x = df["V (V)"]  # 電圧 (V)
        y = df["I (mA)"]  # 電流 (mA)

        # ラベルとタイトルを設定
        plt.xlabel("電圧 (V)")
        plt.ylabel("電流 (mA)")
        # plt.title(f"グラフ{title_suffix}", fontsize=12)

        # グラフを描画
        plt.plot(x, y, "ko", linestyle="solid", lw=1, markersize=3)
        plot_successful = True

    # エラーの場合は画像保存せず終了
    except Exception as e:
        print(f"エラー: {data_path.name} の処理中に問題が発生しました: {e}")

    finally:
        if plot_successful:
            # ファイル名を生成 (元のファイル名から拡張子を除いたものを使用)
            # filename_prefix があればそれも追加
            output_filename = f"{filename_prefix}{data_path.stem}.png"
            output_path = output_dir.joinpath(output_filename)

            # グラフを画像として保存
            try:
                plt.savefig(output_path, bbox_inches="tight", dpi=300)
                print(f"グラフを保存しました: {output_path}")
            except Exception as e:
                print(f"エラー: {output_path} の保存中に問題が発生しました: {e}")
        else:
            # エラーがあった場合は何も保存しない
            print(
                f"情報: {data_path.name} のグラフはエラーのため保存されませんでした。"
            )

        # Figureを閉じる (メモリリークを防ぐため)
        plt.close(fig)


# --- メイン処理 ---
if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    figures_dir = current_dir.joinpath("figures")
    figures_dir.mkdir(parents=True, exist_ok=True)  # ディレクトリがなければ作成

    # グラフ描画するCSVファイルへのパスのリスト
    data_files_info = [
        {
            "path": Path(__file__).resolve().parent.joinpath("data/2-1.csv"),
            "title_suffix": " (Dataset 2-1)",
        },
        {
            "path": Path(__file__).resolve().parent.joinpath("data/2-2.csv"),
            "title_suffix": " (Dataset 2-2)",
        },
        {
            "path": Path(__file__).resolve().parent.joinpath("data/2-3.csv"),
            "title_suffix": " (Dataset 2-3)",
        },
        {
            "path": Path(__file__).resolve().parent.joinpath("data/2-4.csv"),
            "title_suffix": " (Dataset 2-4)",
        },
    ]

    # グラフ設定 (共通)
    plt.rcParams["font.family"] = "Hiragino Mincho ProN"
    # plt.rcParams["font.family"] = "sans-serif" # 汎用的なフォント
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"

    # 各ファイルに対してグラフ描画・保存関数を呼び出し
    for i, file_info in enumerate(data_files_info):
        # ファイル名に連番を振る場合などのために filename_prefix を利用可能
        # prefix = f"plot_{i+1:02d}_"
        plot_and_save_graph(
            data_path=file_info["path"],
            output_dir=figures_dir,
            title_suffix=file_info["title_suffix"],
            # filename_prefix=prefix # 必要であれば接頭辞をつける
        )

    print(
        f"\nすべての処理が完了しました。グラフは '{figures_dir}' に保存されます。"
    )
