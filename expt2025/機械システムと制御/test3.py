from pathlib import Path
import pandas as pd
import numpy as np


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
# 出力ファイル名を今回の定義に合わせて変更
output_csv_file_path = "omega_delta_t_period.csv"  # m が delta_t, n が period なので
crossing_direction = "rising"

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

for current_omega in unique_omegas:
    print(f"\nProcessing omega = {current_omega}...")
    df_filtered = df_all[df_all["omega"] == current_omega].copy()

    # CSV出力用の値を初期化
    output_n_period_seconds = np.nan  # CSVの'n'カラム用 (in の周期 s)
    output_m_time_difference = np.nan  # CSVの'm'カラム用 (生の時刻差 s)

    if df_filtered.empty:
        print(
            f"  Warning: omega = {current_omega} のデータが見つかりません。スキップします。"
        )
        results_list.append(
            {
                "omega": current_omega,
                "m": output_m_time_difference,
                "n": output_n_period_seconds,
            }
        )
        continue

    # 1. 周期の計算 (CSVの 'n' カラム用)
    if current_omega == 0:
        output_n_period_seconds = np.inf
        print(f"  Info: omega = 0 のため、周期 (CSV出力'n'用) は無限大です。")
    else:
        output_n_period_seconds = 2 * np.pi / current_omega
    print(f"  計算された 'in' の周期 (CSV出力'n'用): {output_n_period_seconds:.7g} s")

    # 後続の処理でデータ点数が少ない場合のチェック
    if len(df_filtered) < 2:
        print(
            f"  Warning: omega = {current_omega} のデータ点数が2未満です。時刻差計算 ('m'カラム) をスキップします。"
        )
        results_list.append(
            {
                "omega": current_omega,
                "m": output_m_time_difference,
                "n": output_n_period_seconds,
            }
        )
        continue

    # 2. outの基準線の計算
    out_max = df_filtered["out"].max()
    out_min = df_filtered["out"].min()
    out_baseline = np.nan
    if pd.isna(out_max) or pd.isna(out_min):
        print(
            f"  Warning: omega = {current_omega} の 'out' データにNaNが含まれるか、全てNaNのため、基準線を計算できません。"
        )
    elif out_max == out_min:  # outデータが一定値の場合
        out_baseline = out_max
        print(
            f"  Info: omega = {current_omega} の 'out' データは一定値 ({out_baseline:.5f}) です。基準線は設定されます。"
        )
    else:
        out_baseline = (out_max + out_min) / 2

    # 3. inの基準線の設定
    in_baseline = 0.0

    # 4. 時刻差の計算 (CSVの 'm' カラム用)
    can_calculate_time_diff = True

    if pd.isna(out_baseline):
        print(
            f"  Warning: omega = {current_omega} で 'out' の基準線が計算できなかったため、時刻差計算 ('m'カラム) をスキップします。"
        )
        can_calculate_time_diff = False

    # t_in_ref と t_out_ref の取得
    if can_calculate_time_diff:
        t_in_ref, _ = find_first_crossing_info(
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

    if can_calculate_time_diff:
        t_out_ref, _ = find_first_crossing_info(
            df_filtered["t"],
            df_filtered["out"],
            out_baseline,
            search_start_iloc=0,
            direction=crossing_direction,
        )
        if t_out_ref is None:
            print(
                f"  Warning: omega = {current_omega} で 'out' データの基準線交差 ({crossing_direction} edge) が見つかりませんでした。"
            )
            can_calculate_time_diff = False

    if can_calculate_time_diff:
        # 'm' カラムには、単純な時刻の差 (正規化なし) を格納
        output_m_time_difference = t_out_ref - t_in_ref
        print(f"  計算された時刻差 (CSV出力'm'用): {output_m_time_difference:.7g} s")

    results_list.append(
        {
            "omega": current_omega,
            "m": output_m_time_difference,  # 生の時刻差 (s)
            "n": output_n_period_seconds,  # 'in' の周期 (s)
        }
    )

# 結果をDataFrameに変換してCSVに出力
if results_list:
    results_df = pd.DataFrame(results_list)
    try:
        results_df.to_csv(output_csv_file_path, index=False, float_format="%.7g")
        print(f"\n処理完了。結果は '{output_csv_file_path}' に保存されました。")
        print("出力CSVのカラム: omega, m (in/outの時刻差 s), n (inの周期 s)")
    except Exception as e:
        print(
            f"\nエラー: 結果をCSVファイル '{output_csv_file_path}' に保存できませんでした: {e}"
        )
else:
    print("\n処理対象のomegaデータがなかったため、CSVファイルは出力されませんでした。")
