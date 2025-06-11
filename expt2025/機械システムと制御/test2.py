import pandas as pd
import numpy as np
from pathlib import Path

# matplotlib.pyplot はこのスクリプトでは直接使用しませんが、
# find_first_crossing_info 関数内で将来的にデバッグ用に使う可能性を考慮すると残しても良いです。
# import matplotlib.pyplot as plt # 不要ならコメントアウト


# --- 関数定義 (前回と同じもの) ---
def find_first_crossing_info(
    times_series, data_series, baseline, search_start_iloc=0, direction="rising"
):
    """
    データ系列が指定されたベースラインを特定の方向に最初に横切る情報（時刻と元のインデックス）を見つける。
    「最も近いデータ」とは、横切る直前と直後の点のうち、ベースラインにより近い方の点を指す。
    """
    if search_start_iloc >= len(data_series):
        return None, None

    active_times = times_series.iloc[search_start_iloc:]
    active_data = data_series.iloc[search_start_iloc:]

    if len(active_data) < 2:
        return None, None

    prev_data = active_data.shift(1)
    crossing_condition = None
    if direction == "rising":
        crossing_condition = (prev_data < baseline) & (active_data >= baseline)
    elif direction == "falling":
        crossing_condition = (prev_data > baseline) & (active_data <= baseline)
    else:
        raise ValueError("direction must be 'rising' or 'falling'")

    candidate_indices_original = active_data[crossing_condition].index

    if candidate_indices_original.empty:
        return None, None

    first_crossing_curr_idx_original = candidate_indices_original[0]
    val_curr = active_data.loc[first_crossing_curr_idx_original]
    time_curr = active_times.loc[first_crossing_curr_idx_original]

    loc_curr_in_active = active_data.index.get_loc(first_crossing_curr_idx_original)

    if loc_curr_in_active == 0:
        return time_curr, first_crossing_curr_idx_original

    idx_prev_original = active_data.index[loc_curr_in_active - 1]
    val_prev = active_data.loc[idx_prev_original]
    time_prev = active_times.loc[idx_prev_original]

    if abs(val_curr - baseline) <= abs(val_prev - baseline):
        return time_curr, first_crossing_curr_idx_original
    else:
        return time_prev, idx_prev_original


# --- 設定 ---
input_csv_file_path = (
    Path(__file__).resolve().parent.joinpath("data/20250522_exp_data.csv")
)  # 入力CSVファイル
output_csv_file_path = "omega_m_n_results.csv"  # 出力CSVファイル
crossing_direction = "rising"  # 位相比較のための交差方向 "rising" または "falling"

# --- 処理 ---
try:
    df_all = pd.read_csv(input_csv_file_path)
except FileNotFoundError:
    print(f"エラー: ファイル '{input_csv_file_path}' が見つかりません。")
    exit()
except Exception as e:
    print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    exit()

unique_omegas = sorted(
    df_all["omega"].unique()
)  # omega値をソートして処理順を一定にする
results_list = []

print(
    f"処理開始: 入力ファイル='{input_csv_file_path}', 出力ファイル='{output_csv_file_path}'"
)
print(f"交差方向: {crossing_direction}")

for current_omega in unique_omegas:
    print(f"\nProcessing omega = {current_omega}...")
    df_filtered = df_all[df_all["omega"] == current_omega].copy()

    if df_filtered.empty:
        print(
            f"  Warning: omega = {current_omega} のデータが見つかりません。スキップします。"
        )
        results_list.append({"omega": current_omega, "n": np.nan, "m": np.nan})
        continue

    if len(df_filtered) < 2:  # 交差判定には最低2点必要
        print(
            f"  Warning: omega = {current_omega} のデータ点数が2未満です。位相差計算をスキップします。"
        )
        n_period = 2 * np.pi / current_omega if current_omega != 0 else np.inf
        results_list.append({"omega": current_omega, "n": n_period, "m": np.nan})
        continue

    # 1. 周期nの計算
    if current_omega == 0:
        n_period = np.inf
        print(f"  Info: omega = 0 のため、周期 n は無限大です。")
    else:
        n_period = 2 * np.pi / current_omega
    print(f"  計算された周期 (n): {n_period:.7g} s")

    # 2. outの基準線の計算
    out_max = df_filtered["out"].max()
    out_min = df_filtered["out"].min()

    out_baseline = np.nan
    if pd.isna(out_max) or pd.isna(out_min):
        print(
            f"  Warning: omega = {current_omega} の 'out' データにNaNが含まれるか、全てNaNのため、基準線を計算できません。"
        )
    elif out_max == out_min:
        print(
            f"  Warning: omega = {current_omega} の 'out' データは一定値 ({out_max:.5f}) です。基準線は設定されますが、交差は期待できません。"
        )
        out_baseline = out_max  # または (out_max + out_min) / 2 でも同じ
    else:
        out_baseline = (out_max + out_min) / 2
    # print(f"  Out の基準線: {out_baseline:.5f}") # ログが冗長なのでコメントアウト

    # 3. inの基準線の設定
    in_baseline = 0.0

    # 4. 位相のずれmを求める
    m_current = np.nan  # 初期値はNaN

    if pd.isna(out_baseline):  # out_baselineが計算できなかった場合
        print(
            f"  Warning: omega = {current_omega} で 'out' の基準線が計算できなかったため、位相差計算をスキップします。"
        )
    elif (
        n_period == np.inf or n_period == 0 or pd.isna(n_period)
    ):  # 周期が計算不能な場合
        print(
            f"  Warning: omega = {current_omega} の周期が不定 ({n_period}) のため、位相差計算をスキップします。"
        )
    else:
        # `in` の最初の基準線交差
        t_in_ref, _ = find_first_crossing_info(  # idx_in_ref_original はここでは不要
            df_filtered["t"],
            df_filtered["in"],
            in_baseline,
            search_start_iloc=0,
            direction=crossing_direction,
        )

        # `out` の最初の基準線交差
        t_out_ref, _ = find_first_crossing_info(  # idx_out_ref_original はここでは不要
            df_filtered["t"],
            df_filtered["out"],
            out_baseline,
            search_start_iloc=0,
            direction=crossing_direction,
        )

        if t_in_ref is None:
            print(
                f"  Warning: omega = {current_omega} で 'in' データの基準線交差 ({crossing_direction} edge) が見つかりませんでした。"
            )
        elif t_out_ref is None:
            print(
                f"  Warning: omega = {current_omega} で 'out' データの基準線交差 ({crossing_direction} edge) が見つかりませんでした。"
            )
        else:
            delta_t = t_out_ref - t_in_ref

            # delta_t を [-n/2, n/2] の範囲に正規化
            delta_t_normalized = (delta_t % n_period + n_period) % n_period
            if delta_t_normalized > n_period / 2:
                delta_t_normalized -= n_period

            m_current = (delta_t_normalized / n_period) * (2 * np.pi)
            print(
                f"  計算された位相差 (m): {m_current:.7g} rad ({np.degrees(m_current):.3f} 度)"
            )

    results_list.append({"omega": current_omega, "n": n_period, "m": m_current})

# 結果をDataFrameに変換してCSVに出力
if results_list:
    results_df = pd.DataFrame(results_list)
    try:
        # float_format で出力時の浮動小数点数の桁数を指定
        results_df.to_csv(output_csv_file_path, index=False, float_format="%.7g")
        print(f"\n処理完了。結果は '{output_csv_file_path}' に保存されました。")
    except Exception as e:
        print(
            f"\nエラー: 結果をCSVファイル '{output_csv_file_path}' に保存できませんでした: {e}"
        )
else:
    print("\n処理対象のomegaデータがなかったため、CSVファイルは出力されませんでした。")
