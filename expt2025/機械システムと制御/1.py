import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- 設定 ---
# CSVファイルのパス
data_path = Path(__file__).resolve().parent.joinpath("data/20250522_exp_data.csv")
# 解析対象の角周波数 (この値を変更して異なる角周波数のデータを解析できます)
target_omega = 0.4  # 例: 0.4 rad/s または 0.5 rad/s など

# --- 処理 ---
try:
    df_all = pd.read_csv(data_path)
except FileNotFoundError:
    print(f"エラー: ファイル '{data_path}' が見つかりません。")
    print("指定されたパスにCSVファイルが存在することを確認してください。")
    exit()
except Exception as e:
    print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    print("ファイルの形式（特に区切り文字）を確認してください。")
    exit()

# 指定した角周波数のデータを抽出
df_filtered = df_all[
    df_all["omega"] == target_omega
].copy()  # .copy() をつけてSettingWithCopyWarningを回避

if df_filtered.empty:
    print(
        f"エラー: 指定された角周波数 omega = {target_omega} のデータが見つかりませんでした。"
    )
    print(f"CSVファイル内の利用可能なomega値: {df_all['omega'].unique()}")
    exit()

# 抽出されたデータから角周波数を取得（target_omega と同じはずだが、念のため）
# この angular_frequency_omega は周期計算に直接使用する
angular_frequency_omega = target_omega
print(f"解析対象の角周波数 (omega): {angular_frequency_omega} rad/s")

# 周期 T = 2 * pi / omega
# この周期を 変数 n に格納する
n = 2 * np.pi / angular_frequency_omega

print(f"理想応答(in)の計算された周期 (n) for omega={target_omega}: {n:.5f} s")

# --- 結果の確認（任意：プロット） ---
# 抽出されたデータでプロット
if (
    not df_filtered.empty
    and "t" in df_filtered.columns
    and "in" in df_filtered.columns
    and len(df_filtered["t"]) > 1
):
    plt.figure(figsize=(12, 7))
    plt.plot(
        df_filtered["t"],
        df_filtered["in"],
        label=f"Ideal Response (in) for ω={target_omega}",
        marker=".",
        linestyle="-",
    )
    plt.title(
        f"Ideal Response (in) vs. Time for ω = {angular_frequency_omega:.2f} rad/s\nCalculated Period (n) = {n:.3f} s"
    )
    plt.xlabel("Time (t) [s]")
    plt.ylabel("Ideal Response (in)")

    # 周期の視覚的確認のために、最初の点から1周期分、2周期分の位置に縦線を描画
    # フィルタリングされたデータの最初の時刻を開始点とする
    if not df_filtered["t"].empty:
        first_time_point_filtered = df_filtered["t"].iloc[0]
        plt.axvline(
            first_time_point_filtered,
            color="gray",
            linestyle=":",
            linewidth=1,
            label=f"t_start_filtered = {first_time_point_filtered:.2f}s",
        )

        # 1周期後の線
        period_line_1 = first_time_point_filtered + n
        if (
            period_line_1 <= df_filtered["t"].max() + n * 0.1
        ):  # プロット範囲内に収まるように少し余裕を持たせる
            plt.axvline(
                period_line_1,
                color="red",
                linestyle="--",
                linewidth=1,
                label=f"t_start + n (1 period) = {period_line_1:.2f}s",
            )

        # 2周期後の線 (データが十分にあれば)
        period_line_2 = first_time_point_filtered + 2 * n
        if (
            period_line_2 <= df_filtered["t"].max() + n * 0.1
        ):  # プロット範囲内に収まるように少し余裕を持たせる
            plt.axvline(
                period_line_2,
                color="purple",
                linestyle="--",
                linewidth=1,
                label=f"t_start + 2n (2 periods) = {period_line_2:.2f}s",
            )

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print(
        f"プロットに必要なデータが不足しているか、't'または'in'カラムがありません (omega={target_omega} のデータ)。"
    )
