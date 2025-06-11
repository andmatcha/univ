import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- グラフ設定 ---
plt.rcParams["font.family"] = "Hiragino Mincho ProN"
plt.rcParams["xtick.direction"] = "in"
plt.rcParams["ytick.direction"] = "in"

# --- 設定 ---
input_csv_file_path = (
    Path(__file__).resolve().parent.joinpath("data/20250522_exp_data.csv")
)
output_csv_file_path_gain = "omega_gain_analysis.csv"
plot_output_filename_gain = "omega_vs_gain_plot.png"

# --- 処理 ---
try:
    df_all = pd.read_csv(input_csv_file_path)
except FileNotFoundError:
    print(f"エラー: ファイル '{input_csv_file_path}' が見つかりません。")
    exit()
except Exception as e:
    print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    exit()

unique_omegas = sorted(df_all["omega"].unique())
gain_results_list = []

print(
    f"処理開始 (ゲイン解析): 入力ファイル='{input_csv_file_path}', 出力ファイル='{output_csv_file_path_gain}'"
)

for current_omega in unique_omegas:
    print(f"\nProcessing omega = {current_omega} for gain analysis...")
    df_filtered = df_all[df_all["omega"] == current_omega].copy()

    A_in = np.nan
    A_out = np.nan
    gain_db = np.nan

    if df_filtered.empty:
        print(
            f"  Warning: omega = {current_omega} のデータが見つかりません。スキップします。"
        )
        gain_results_list.append(
            {"omega": current_omega, "A_in": A_in, "A_out": A_out, "gain": gain_db}
        )
        continue

    if len(df_filtered) < 2:  # 振幅計算には最低2点ある方が望ましい（max/minのため）
        print(
            f"  Warning: omega = {current_omega} のデータ点数が2未満です。振幅・ゲイン計算をスキップします。"
        )
        gain_results_list.append(
            {"omega": current_omega, "A_in": A_in, "A_out": A_out, "gain": gain_db}
        )
        continue

    # 1. A_in (inの振幅) の計算
    in_max = df_filtered["in"].max()
    in_min = df_filtered["in"].min()
    if pd.isna(in_max) or pd.isna(in_min):
        print(
            f"  Warning: omega = {current_omega} の 'in' データにNaNが含まれるため、A_inを計算できません。"
        )
    elif in_max == in_min:  # 振幅が0またはデータが1点しかない場合
        A_in = 0.0
        print(
            f"  Info: omega = {current_omega} の 'in' データは一定値 ({in_max:.5f}) または振幅ゼロです。A_in = 0.0"
        )
    else:
        A_in = (in_max - in_min) / 2.0
    print(f"  A_in: {A_in:.7g}")

    # 2. A_out (outの振幅) の計算
    out_max = df_filtered["out"].max()
    out_min = df_filtered["out"].min()
    if pd.isna(out_max) or pd.isna(out_min):
        print(
            f"  Warning: omega = {current_omega} の 'out' データにNaNが含まれるため、A_outを計算できません。"
        )
    elif out_max == out_min:  # 振幅が0またはデータが1点しかない場合
        A_out = 0.0
        print(
            f"  Info: omega = {current_omega} の 'out' データは一定値 ({out_max:.5f}) または振幅ゼロです。A_out = 0.0"
        )
    else:
        A_out = (out_max - out_min) / 2.0
    print(f"  A_out: {A_out:.7g}")

    # 3. ゲインの計算 (dB)
    if pd.isna(A_in) or pd.isna(A_out):
        print(
            f"  Info: A_in または A_out が計算できなかったため、ゲインは計算されません。"
        )
    elif A_in == 0:
        if A_out == 0:
            gain_db = (
                0.0  # 0/0 の場合はゲイン0dB (1倍) とみなすか、定義による（ここでは0dB）
            )
            print(f"  Info: A_in = 0 かつ A_out = 0 のため、ゲインを 0.0 dB とします。")
        else:
            gain_db = np.inf  # 0で割るため無限大（またはエラー）
            print(f"  Warning: A_in = 0 かつ A_out != 0 のため、ゲインは無限大です。")
    elif A_out == 0:  # A_in !=0 and A_out == 0
        gain_db = -np.inf  # ログの中身が0になるため負の無限大
        print(f"  Info: A_out = 0 かつ A_in !=0 のため、ゲインは -無限大 dB です。")

    else:  # A_in > 0 and A_out > 0 (または A_out < 0 だが振幅なので絶対値で考える)
        gain_ratio = A_out / A_in
        if gain_ratio > 0:  # log10 の引数は正である必要がある
            gain_db = 20 * np.log10(gain_ratio)
            print(f"  Gain: {gain_db:.7g} dB")
        else:  # A_out/A_in <= 0 (理論上は振幅なので起こらないはずだが念のため)
            gain_db = -np.inf  # またはエラー処理
            print(
                f"  Warning: A_out/A_in ({gain_ratio}) が非正のため、ゲイン計算でエラー（-infを設定）。"
            )

    gain_results_list.append(
        {"omega": current_omega, "A_in": A_in, "A_out": A_out, "gain": gain_db}
    )

# 結果をDataFrameに変換してCSVに出力
if gain_results_list:
    gain_results_df = pd.DataFrame(gain_results_list)
    try:
        gain_results_df.to_csv(
            output_csv_file_path_gain, index=False, float_format="%.7g"
        )
        print(
            f"\n処理完了。ゲイン解析結果は '{output_csv_file_path_gain}' に保存されました。"
        )
    except Exception as e:
        print(
            f"\nエラー: 結果をCSVファイル '{output_csv_file_path_gain}' に保存できませんでした: {e}"
        )

    # ゲイン線図のプロット
    # NaNやinfを除外してプロット
    plot_gain_df = gain_results_df.replace([np.inf, -np.inf], np.nan).dropna(
        subset=["omega", "gain"]
    )

    if (
        not plot_gain_df.empty and not plot_gain_df["omega"].eq(0).all()
    ):  # omegaが全て0でないことも確認
        plt.figure(figsize=(10, 6))
        # omegaが0を含む場合、logスケールでエラーになるため、0より大きいomegaのみをプロット対象とする
        plot_data_valid_omega = plot_gain_df[plot_gain_df["omega"] > 0]
        if not plot_data_valid_omega.empty:
            plt.semilogx(
                plot_data_valid_omega["omega"],
                plot_data_valid_omega["gain"],
                marker="o",
                linestyle="-",
                color="black",  # グラフの色を黒に設定
            )
            # plt.title("Gain Diagram (Bode Plot - Magnitude)") # グラフタイトルを削除
            plt.xlabel(
                "角周波数 (rad / s)", fontsize=14
            )  # 横軸タイトルのフォントサイズ変更
            plt.ylabel("ゲイン (dB)", fontsize=14)  # 縦軸タイトルのフォントサイズ変更
            try:
                plt.savefig(plot_output_filename_gain)
                print(f"ゲイン線図は '{plot_output_filename_gain}' に保存されました。")
            except Exception as e:
                print(
                    f"エラー: ゲイン線図をファイル '{plot_output_filename_gain}' に保存できませんでした: {e}"
                )
            plt.show()
        else:
            print("プロット対象のomega > 0 の有効なデータがありませんでした。")
    elif plot_gain_df.empty:
        print(
            "ゲイン線図のプロット対象の有効なデータがありませんでした（'omega'または'gain'がNaN/inf）。"
        )
    else:  # omegaが全て0の場合など
        print(
            "omegaが0のみ、または有効なデータがないため、対数スケールでのゲイン線図はプロットできません。"
        )
else:
    print(
        "\n処理対象のomegaデータがなかったため、CSVファイルおよびゲイン線図は出力されませんでした。"
    )
