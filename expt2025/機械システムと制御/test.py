import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# --- 関数定義 ---
def find_first_crossing_info(
    times_series, data_series, baseline, search_start_iloc=0, direction="rising"
):
    """
    データ系列が指定されたベースラインを特定の方向に最初に横切る情報（時刻と元のインデックス）を見つける。
    「最も近いデータ」とは、横切る直前と直後の点のうち、ベースラインにより近い方の点を指す。

    Args:
        times_series (pd.Series): 時刻データ (例: df_filtered['t'])
        data_series (pd.Series): 信号データ (例: df_filtered['in'] または df_filtered['out'])
        baseline (float): 基準線
        search_start_iloc (int): times_series/data_series の .iloc インデックスでの検索開始位置
        direction (str): "rising" (上昇)、"falling" (下降)

    Returns:
        tuple (float, object) or (None, None): (交差時刻, 元のDataFrameでのインデックス)。見つからなければ (None, None)。
    """
    if search_start_iloc >= len(data_series):  # 開始位置がデータ長以上ならデータなし
        return None, None

    # search_start_iloc 以降のデータを対象とする
    # .iloc スライスはコピーを返し、元のインデックスは保持される
    active_times = times_series.iloc[search_start_iloc:]
    active_data = data_series.iloc[search_start_iloc:]

    if len(active_data) < 2:  # prevと比較するために最低2点必要
        return None, None

    # prev_data は active_data の1つ前の値を持ち、インデックスは active_data に揃う
    # active_data.iloc[0] に対応する prev_data.iloc[0] は NaN になる
    prev_data = active_data.shift(1)

    crossing_condition = None
    if direction == "rising":
        # prev < baseline かつ curr >= baseline
        crossing_condition = (prev_data < baseline) & (active_data >= baseline)
    elif direction == "falling":
        # prev > baseline かつ curr <= baseline
        crossing_condition = (prev_data > baseline) & (active_data <= baseline)
    else:
        raise ValueError("direction must be 'rising' or 'falling'")

    # crossing_condition が True となるインデックスのリスト (これらは元のDataFrameのインデックス)
    candidate_indices_original = active_data[crossing_condition].index

    if candidate_indices_original.empty:
        return None, None  # 交差が見つからない

    # 最初の交差が発生した点 (curr) の元のインデックス
    first_crossing_curr_idx_original = candidate_indices_original[0]

    val_curr = active_data.loc[first_crossing_curr_idx_original]
    time_curr = active_times.loc[first_crossing_curr_idx_original]

    # 前の点のインデックスを取得
    # active_data における first_crossing_curr_idx_original の .iloc 位置を探す
    loc_curr_in_active = active_data.index.get_loc(first_crossing_curr_idx_original)

    if loc_curr_in_active == 0:
        # active_data の最初の点が交差後の点だった場合。
        # これは prev_data.iloc[0] が NaN のため、crossing_condition で除外されるはず。
        # もし何らかの理由でここに来た場合、前の点がないので現在の点を採用
        return time_curr, first_crossing_curr_idx_original

    # active_data.index[loc_curr_in_active - 1] で前の点の元のインデックスが取れる
    idx_prev_original = active_data.index[loc_curr_in_active - 1]

    val_prev = active_data.loc[idx_prev_original]
    time_prev = active_times.loc[idx_prev_original]

    # ベースラインに近い方を選ぶ
    if abs(val_curr - baseline) <= abs(
        val_prev - baseline
    ):  # 等しい場合はcurr (交差後の点) を優先
        return time_curr, first_crossing_curr_idx_original
    else:
        return time_prev, idx_prev_original


# --- 設定 ---
csv_file_path = Path(__file__).resolve().parent.joinpath("data/20250522_exp_data.csv")
target_omega = 32  # 解析対象の角周波数
crossing_direction = "rising"  # 位相比較のための交差方向 "rising" または "falling"

# --- 1. CSVファイルの読み込みとフィルタリング、周期nの計算 ---
try:
    df_all = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"エラー: ファイル '{csv_file_path}' が見つかりません。")
    exit()
except Exception as e:
    print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    exit()

df_filtered = df_all[df_all["omega"] == target_omega].copy()

if df_filtered.empty:
    print(
        f"エラー: 指定された角周波数 omega = {target_omega} のデータが見つかりませんでした。"
    )
    exit()

# 元のインデックスを保持したまま操作するため、インデックスのリセットは行わない

angular_frequency_omega = target_omega  # df_filtered['omega'].iloc[0] でも可
n = 2 * np.pi / angular_frequency_omega
print(f"解析対象の角周波数 (omega): {angular_frequency_omega} rad/s")
print(f"理想応答(in)の計算された周期 (n): {n:.5f} s")

# --- 2. outの基準線の計算 ---
out_max = df_filtered["out"].max()
out_min = df_filtered["out"].min()
out_baseline = (out_max + out_min) / 2
print(f"Out の基準線 (max+min)/2: {out_baseline:.5f}")

# --- 3. inの基準線の設定 ---
in_baseline = 0.0
print(f"In の基準線: {in_baseline:.1f}")

# --- 4. 同じ周期内のinとoutの位相のずれを求める ---
# `in` の最初の基準線交差時刻と、その時刻に対応する元のDataFrameでのインデックスを取得
# search_start_iloc=0 は df_filtered の先頭から検索を開始するという意味
t_in_ref, idx_in_ref_original = find_first_crossing_info(
    df_filtered["t"],
    df_filtered["in"],
    in_baseline,
    search_start_iloc=0,
    direction=crossing_direction,
)

if t_in_ref is None:
    print(
        f"エラー: 'in'データで基準線との交差 ({crossing_direction} edge) が見つかりませんでした。"
    )
    print("crossing_direction を変更するか、データを確認してください。")
    exit()
print(
    f"In の最初の基準線交差 ({crossing_direction} edge): t = {t_in_ref:.5f} s (元のデータ点インデックス: {idx_in_ref_original})"
)

# `out` の最初の基準線交差時刻とインデックス
t_out_ref, idx_out_ref_original = find_first_crossing_info(
    df_filtered["t"],
    df_filtered["out"],
    out_baseline,
    search_start_iloc=0,
    direction=crossing_direction,
)

if t_out_ref is None:
    print(
        f"エラー: 'out'データで基準線との交差 ({crossing_direction} edge) が見つかりませんでした。"
    )
    print("crossing_direction を変更するか、データを確認してください。")
    exit()
print(
    f"Out の最初の基準線交差 ({crossing_direction} edge): t = {t_out_ref:.5f} s (元のデータ点インデックス: {idx_out_ref_original})"
)

# 時刻差の計算
delta_t = t_out_ref - t_in_ref
print(f"参照点間の初期時間差 (delta_t = t_out_ref - t_in_ref): {delta_t:.5f} s")

# delta_t を [-n/2, n/2] の範囲に正規化
# これにより、1周期以上ずれた交差点を拾った場合でも、最も近い位相差に補正する
delta_t_normalized = (delta_t % n + n) % n  # delta_t を [0, n) の範囲へマッピング
if delta_t_normalized > n / 2:
    delta_t_normalized -= n  # さらに (-n/2, n/2] の範囲へマッピング

print(f"正規化された時間差 (delta_t_normalized): {delta_t_normalized:.5f} s")

# 位相差 m の計算 (ラジアン単位)
m = (delta_t_normalized / n) * (2 * np.pi)
print(f"計算された位相差 (m): {m:.5f} rad ({np.degrees(m):.2f} 度)")

# --- 5. プロットで確認 ---
plt.figure(figsize=(14, 8))

# In のプロット
plt.plot(
    df_filtered["t"],
    df_filtered["in"],
    label=f"Ideal Response (in) for ω={target_omega}",
    marker=".",
    linestyle="-",
    color="blue",
    alpha=0.7,
)
plt.axhline(
    in_baseline,
    color="blue",
    linestyle=":",
    linewidth=1.5,
    label=f"In Baseline ({in_baseline:.2f})",
)
if t_in_ref is not None:
    # .loc を使って元のインデックスで値を取得
    plt.scatter(
        [t_in_ref],
        [df_filtered.loc[idx_in_ref_original, "in"]],
        color="cyan",
        s=120,
        zorder=5,
        edgecolor="black",
        label=f"In Ref Point (t={t_in_ref:.3f}s)",
    )

# Out のプロット
plt.plot(
    df_filtered["t"],
    df_filtered["out"],
    label=f"Actual Response (out) for ω={target_omega}",
    marker=".",
    linestyle="-",
    color="red",
    alpha=0.7,
)
plt.axhline(
    out_baseline,
    color="red",
    linestyle=":",
    linewidth=1.5,
    label=f"Out Baseline ({out_baseline:.3f})",
)
if t_out_ref is not None:
    plt.scatter(
        [t_out_ref],
        [df_filtered.loc[idx_out_ref_original, "out"]],
        color="magenta",
        s=120,
        zorder=5,
        edgecolor="black",
        label=f"Out Ref Point (t={t_out_ref:.3f}s)",
    )

# 周期の視覚化 (オプション)
if t_in_ref is not None:
    plt.axvline(t_in_ref, color="gray", linestyle="--", linewidth=0.8)
    plt.axvline(
        t_in_ref + n,
        color="gray",
        linestyle="--",
        linewidth=0.8,
        label=f"One period (n={n:.2f}s) from In Ref",
    )

plt.title(
    f"In/Out Responses and Reference Points for ω={target_omega}\nCalculated Period n={n:.3f}s, Phase Difference m={m:.3f}rad ({np.degrees(m):.1f}°)"
)
plt.xlabel("Time (t) [s]")
plt.ylabel("Response Value")
plt.legend(loc="best")
plt.grid(True)
plt.tight_layout()
plt.show()
