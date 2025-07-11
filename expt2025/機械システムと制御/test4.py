from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# --- 関数定義 (前回と同じもの、ilocも返すように修正) ---
def find_first_crossing_info_with_iloc(
    times_series, data_series, baseline, search_start_iloc=0, direction="rising"
):
    """
    データ系列が指定されたベースラインを特定の方向に最初に横切る情報（時刻、元のインデックス、.iloc位置）を見つける。
    「最も近いデータ」とは、横切る直前と直後の点のうち、ベースラインにより近い方の点を指す。

    Args:
        times_series (pd.Series): 時刻データ (例: df_filtered['t'])
        data_series (pd.Series): 信号データ (例: df_filtered['in'] または df_filtered['out'])
        baseline (float): 基準線
        search_start_iloc (int): times_series/data_series の .iloc インデックスでの検索開始位置
        direction (str): "rising" (上昇)、"falling" (下降)

    Returns:
        tuple (float, object, int) or (None, None, None): (交差時刻, 元のDataFrameでのインデックス, df_filteredでの.iloc位置)。
                                                            見つからなければ (None, None, None)。
    """
    if search_start_iloc >= len(data_series):
        return None, None, None

    # search_start_iloc 以降のデータを対象とする
    active_times = times_series.iloc[search_start_iloc:]
    active_data = data_series.iloc[search_start_iloc:]

    if len(active_data) < 2:
        return None, None, None

    prev_data = active_data.shift(1)
    crossing_condition = None
    if direction == "rising":
        crossing_condition = (prev_data < baseline) & (active_data >= baseline)
    elif direction == "falling":
        crossing_condition = (prev_data > baseline) & (active_data <= baseline)
    else:
        raise ValueError("direction must be 'rising' or 'falling'")

    # crossing_condition が True となるインデックスのリスト (これらは元のDataFrameのインデックス)
    candidate_indices_original = active_data[crossing_condition].index

    if candidate_indices_original.empty:
        return None, None, None  # 交差が見つからない

    # 最初の交差が発生した点 (curr) の元のインデックス
    first_crossing_curr_idx_original = candidate_indices_original[0]

    val_curr = active_data.loc[first_crossing_curr_idx_original]
    time_curr = active_times.loc[first_crossing_curr_idx_original]

    # active_data における first_crossing_curr_idx_original の .iloc 位置を探す
    loc_curr_in_active = active_data.index.get_loc(first_crossing_curr_idx_original)

    # df_filtered全体での.iloc位置に変換
    iloc_curr_in_df_filtered = search_start_iloc + loc_curr_in_active

    if loc_curr_in_active == 0:
        return time_curr, first_crossing_curr_idx_original, iloc_curr_in_df_filtered

    # active_data.index[loc_curr_in_active - 1] で前の点の元のインデックスが取れる
    idx_prev_original = active_data.index[loc_curr_in_active - 1]
    iloc_prev_in_df_filtered = search_start_iloc + loc_curr_in_active - 1

    val_prev = active_data.loc[idx_prev_original]
    time_prev = active_times.loc[idx_prev_original]

    # ベースラインに近い方を選ぶ
    if abs(val_curr - baseline) <= abs(val_prev - baseline):
        return time_curr, first_crossing_curr_idx_original, iloc_curr_in_df_filtered
    else:
        return time_prev, idx_prev_original, iloc_prev_in_df_filtered


# --- 設定 ---
input_csv_file_path = (
    Path(__file__).resolve().parent.joinpath("data/20250522_exp_data.csv")
)
output_csv_file_path = "omega_analysis_results_out_after_in.csv"  # ファイル名変更
crossing_direction = "falling"
plot_output_filename = "omega_vs_phase_plot_out_after_in.png"  # プロットファイル名変更

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
results_list = []

print(
    f"処理開始: 入力ファイル='{input_csv_file_path}', 出力ファイル='{output_csv_file_path}'"
)
print(f"交差方向: {crossing_direction}")
print(f"m (時刻差) の計算時、outの交差はinの交差以降から探索します。")


for current_omega in unique_omegas:
    print(f"\nProcessing omega = {current_omega}...")
    df_filtered = df_all[
        df_all["omega"] == current_omega
    ].copy()  # df_filteredのインデックスはdf_allと同じ

    output_n_period_seconds = np.nan
    output_m_time_difference = np.nan
    output_phase_degrees = np.nan

    if df_filtered.empty:
        print(
            f"  Warning: omega = {current_omega} のデータが見つかりません。スキップします。"
        )
        results_list.append(
            {
                "omega": current_omega,
                "m": output_m_time_difference,
                "n": output_n_period_seconds,
                "phase": output_phase_degrees,
            }
        )
        continue

    if current_omega == 0:
        output_n_period_seconds = np.inf
    else:
        output_n_period_seconds = 2 * np.pi / current_omega
    print(f"  計算された 'in' の周期 (CSV出力'n'用): {output_n_period_seconds:.7g} s")

    if len(df_filtered) < 2:
        print(
            f"  Warning: omega = {current_omega} のデータ点数が2未満です。時刻差計算 ('m'カラム) と位相計算をスキップします。"
        )
        results_list.append(
            {
                "omega": current_omega,
                "m": output_m_time_difference,
                "n": output_n_period_seconds,
                "phase": output_phase_degrees,
            }
        )
        continue

    out_max = df_filtered["out"].max()
    out_min = df_filtered["out"].min()
    out_baseline = np.nan
    if pd.isna(out_max) or pd.isna(out_min):
        print(f"  Warning: omega = {current_omega} の 'out' データ基準線計算不可。")
    elif out_max == out_min:
        out_baseline = out_max
    else:
        out_baseline = (out_max + out_min) / 2
    in_baseline = 0.0

    can_calculate_time_diff = True
    t_in_ref = None
    iloc_in_ref_in_df_filtered = None  # df_filtered での .iloc 位置を保持

    if pd.isna(out_baseline):
        print(
            f"  Warning: 'out'基準線計算不可のため、時刻差計算 ('m'カラム) と位相計算をスキップします。"
        )
        can_calculate_time_diff = False

    if can_calculate_time_diff:
        # in の最初の交差を探す (df_filtered の先頭から)
        t_in_ref, _, iloc_in_ref_in_df_filtered = find_first_crossing_info_with_iloc(
            df_filtered["t"],
            df_filtered["in"],
            in_baseline,
            search_start_iloc=0,
            direction=crossing_direction,
        )
        if t_in_ref is None:
            print(
                f"  Warning: omega = {current_omega} で 'in' データの基準線交差 ({crossing_direction} edge) が見つかりませんでした。"
            )
            can_calculate_time_diff = False
        else:
            print(
                f"  'in' 交差発見: t={t_in_ref:.5f} s (df_filtered.iloc[{iloc_in_ref_in_df_filtered}])"
            )

    if can_calculate_time_diff:
        # out の交差を in の交差位置以降から探す
        # iloc_in_ref_in_df_filtered を開始点とする (同じ点でも良い)
        search_start_for_out = iloc_in_ref_in_df_filtered
        print(
            f"  'out' 交差探索開始: df_filtered.iloc[{search_start_for_out}] (時刻 {df_filtered['t'].iloc[search_start_for_out]:.5f} s) 以降"
        )

        t_out_ref, _, _ = (
            find_first_crossing_info_with_iloc(  # iloc_out_ref はここでは不要
                df_filtered["t"],
                df_filtered["out"],
                out_baseline,
                search_start_iloc=search_start_for_out,
                direction=crossing_direction,
            )
        )
        if t_out_ref is None:
            print(
                f"  Warning: omega = {current_omega} で 'in' の交差以降に 'out' データの基準線交差 ({crossing_direction} edge) が見つかりませんでした。"
            )
            can_calculate_time_diff = False
        else:
            print(f"  'out' 交差発見: t={t_out_ref:.5f} s")

    if can_calculate_time_diff:
        output_m_time_difference = t_out_ref - t_in_ref
        print(f"  計算された時刻差 (CSV出力'm'用): {output_m_time_difference:.7g} s")

        if not (
            pd.isna(output_m_time_difference)
            or pd.isna(output_n_period_seconds)
            or output_n_period_seconds == 0
            or np.isinf(output_n_period_seconds)
        ):
            output_phase_degrees = (
                -360 * output_m_time_difference / output_n_period_seconds
            )
            print(f"  計算された位相 (CSV出力'phase'用): {output_phase_degrees:.7g} 度")
        else:
            print(
                f"  Info: 時刻差 ('m') または周期 ('n') が不適切なため、位相 ('phase') は計算されませんでした。"
            )

    results_list.append(
        {
            "omega": current_omega,
            "m": output_m_time_difference,
            "n": output_n_period_seconds,
            "phase": output_phase_degrees,
        }
    )

# 結果をDataFrameに変換してCSVに出力
if results_list:
    results_df = pd.DataFrame(results_list)
    try:
        results_df.to_csv(output_csv_file_path, index=False, float_format="%.7g")
        print(f"\n処理完了。結果は '{output_csv_file_path}' に保存されました。")
    except Exception as e:
        print(
            f"\nエラー: 結果をCSVファイル '{output_csv_file_path}' に保存できませんでした: {e}"
        )

    plot_df = results_df.dropna(subset=["omega", "phase"])
    if not plot_df.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(plot_df["omega"], plot_df["phase"], marker="o", linestyle="-")
        plt.title(
            "Phase vs. Angular Frequency (Omega)\n(out crossing searched after in crossing)"
        )
        plt.xlabel("Angular Frequency (omega) [rad/s]")
        plt.ylabel("Phase [degrees]")
        plt.grid(True)
        plt.tight_layout()
        try:
            plt.savefig(plot_output_filename)
            print(f"グラフは '{plot_output_filename}' に保存されました。")
        except Exception as e:
            print(
                f"エラー: グラフをファイル '{plot_output_filename}' に保存できませんでした: {e}"
            )
        plt.show()
    else:
        print("プロット対象の有効なデータがありませんでした。")
else:
    print(
        "\n処理対象のomegaデータがなかったため、CSVファイルおよびグラフは出力されませんでした。"
    )
