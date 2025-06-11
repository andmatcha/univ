import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- 設定 ---
input_csv_file_path = (
    Path(__file__).resolve().parent.joinpath("data/20250522_exp_data.csv")
)
target_omega_for_amplitude_plot = 0.4  # 振幅を図示したいomegaの値を指定

# --- 処理 ---
try:
    df_all = pd.read_csv(input_csv_file_path)
except FileNotFoundError:
    print(f"エラー: ファイル '{input_csv_file_path}' が見つかりません。")
    exit()
except Exception as e:
    print(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
    exit()

# 指定したomegaのデータをフィルタリング
df_selected = df_all[df_all["omega"] == target_omega_for_amplitude_plot].copy()

if df_selected.empty:
    print(
        f"エラー: 指定された角周波数 omega = {target_omega_for_amplitude_plot} のデータが見つかりませんでした。"
    )
    print(f"CSVファイル内の利用可能なomega値: {df_all['omega'].unique()}")
    exit()

if len(df_selected) < 2:
    print(
        f"エラー: omega = {target_omega_for_amplitude_plot} のデータ点数が2未満のため、振幅の図示が困難です。"
    )
    exit()

print(f"--- omega = {target_omega_for_amplitude_plot} の振幅解析と図示 ---")

# --- 'in' データの解析と図示準備 ---
in_data = df_selected["in"]
t_data_in = df_selected["t"]

in_max_val = in_data.max()
in_min_val = in_data.min()
A_in = np.nan

if pd.isna(in_max_val) or pd.isna(in_min_val):
    print("'in' データにNaNが含まれるため、振幅を計算・図示できません。")
elif in_max_val == in_min_val:
    A_in = 0.0
    print(f"'in' データは一定値 ({in_max_val:.5f})。振幅 A_in = 0.0")
    # 最大/最小位置の取得 (複数の場合があるため最初のものを採用)
    idx_in_max = in_data[in_data == in_max_val].index[0]
    idx_in_min = in_data[in_data == in_min_val].index[
        0
    ]  # この場合 idx_in_max と同じはず
    t_in_max = df_selected.loc[idx_in_max, "t"]
    t_in_min = df_selected.loc[idx_in_min, "t"]  # この場合 t_in_max と同じはず
else:
    A_in = (in_max_val - in_min_val) / 2.0
    print(f"A_in (振幅): {A_in:.5f} (max: {in_max_val:.5f}, min: {in_min_val:.5f})")
    # 最大値・最小値が発生した最初のインデックスと時刻を取得
    idx_in_max = in_data.idxmax()  # 最初の最大値のインデックス
    idx_in_min = in_data.idxmin()  # 最初の最小値のインデックス
    t_in_max = df_selected.loc[idx_in_max, "t"]
    t_in_min = df_selected.loc[idx_in_min, "t"]
    in_baseline_val = (in_max_val + in_min_val) / 2.0  # 振幅計算の基準線

# --- 'out' データの解析と図示準備 ---
out_data = df_selected["out"]
t_data_out = df_selected["t"]  # 時刻軸は共通と仮定

out_max_val = out_data.max()
out_min_val = out_data.min()
A_out = np.nan

if pd.isna(out_max_val) or pd.isna(out_min_val):
    print("'out' データにNaNが含まれるため、振幅を計算・図示できません。")
elif out_max_val == out_min_val:
    A_out = 0.0
    print(f"'out' データは一定値 ({out_max_val:.5f})。振幅 A_out = 0.0")
    idx_out_max = out_data[out_data == out_max_val].index[0]
    idx_out_min = out_data[out_data == out_min_val].index[0]
    t_out_max = df_selected.loc[idx_out_max, "t"]
    t_out_min = df_selected.loc[idx_out_min, "t"]
else:
    A_out = (out_max_val - out_min_val) / 2.0
    print(f"A_out (振幅): {A_out:.5f} (max: {out_max_val:.5f}, min: {out_min_val:.5f})")
    idx_out_max = out_data.idxmax()
    idx_out_min = out_data.idxmin()
    t_out_max = df_selected.loc[idx_out_max, "t"]
    t_out_min = df_selected.loc[idx_out_min, "t"]
    out_baseline_val = (out_max_val + out_min_val) / 2.0


# --- グラフ描画 ---
fig, axs = plt.subplots(2, 1, figsize=(12, 10), sharex=True)  # 2つの縦並びサブプロット

# 'in' のプロット
axs[0].plot(
    t_data_in,
    in_data,
    label=f"in (ω={target_omega_for_amplitude_plot})",
    color="blue",
    marker=".",
)
if not pd.isna(A_in) and A_in > 0:  # 振幅が計算できて0より大きい場合のみ
    axs[0].scatter(
        [t_in_max, t_in_min],
        [in_max_val, in_min_val],
        color="red",
        s=100,
        zorder=5,
        label="Max/Min Points",
    )
    axs[0].hlines(
        in_max_val,
        t_data_in.min(),
        t_data_in.max(),
        colors="red",
        linestyles="dotted",
        lw=1,
    )
    axs[0].hlines(
        in_min_val,
        t_data_in.min(),
        t_data_in.max(),
        colors="red",
        linestyles="dotted",
        lw=1,
    )
    axs[0].hlines(
        in_baseline_val,
        t_data_in.min(),
        t_data_in.max(),
        colors="gray",
        linestyles="dashed",
        lw=1,
        label=f"Baseline ({in_baseline_val:.3f})",
    )
    # 振幅を図示 (矢印とテキスト) - 代表的な1箇所に
    # 最小値からベースラインまでの矢印
    axs[0].annotate(
        "",
        xy=(t_in_min, in_baseline_val),
        xytext=(t_in_min, in_min_val),
        arrowprops=dict(arrowstyle="<->", color="green", lw=1.5),
    )
    axs[0].text(
        t_in_min + (t_data_in.max() - t_data_in.min()) * 0.02,
        in_min_val + A_in / 2,
        f"A_in={A_in:.3f}",
        color="green",
        va="center",
    )
elif not pd.isna(A_in) and A_in == 0:  # 振幅が0の場合
    axs[0].hlines(
        in_max_val,
        t_data_in.min(),
        t_data_in.max(),
        colors="gray",
        linestyles="dashed",
        lw=1,
        label=f"Constant Value ({in_max_val:.3f})",
    )


axs[0].set_title(
    f"Input (in) Signal and Amplitude for ω = {target_omega_for_amplitude_plot}"
)
axs[0].set_ylabel("in Value")
axs[0].legend()
axs[0].grid(True)

# 'out' のプロット
axs[1].plot(
    t_data_out,
    out_data,
    label=f"out (ω={target_omega_for_amplitude_plot})",
    color="orange",
    marker=".",
)
if not pd.isna(A_out) and A_out > 0:
    axs[1].scatter(
        [t_out_max, t_out_min],
        [out_max_val, out_min_val],
        color="purple",
        s=100,
        zorder=5,
        label="Max/Min Points",
    )
    axs[1].hlines(
        out_max_val,
        t_data_out.min(),
        t_data_out.max(),
        colors="purple",
        linestyles="dotted",
        lw=1,
    )
    axs[1].hlines(
        out_min_val,
        t_data_out.min(),
        t_data_out.max(),
        colors="purple",
        linestyles="dotted",
        lw=1,
    )
    axs[1].hlines(
        out_baseline_val,
        t_data_out.min(),
        t_data_out.max(),
        colors="gray",
        linestyles="dashed",
        lw=1,
        label=f"Baseline ({out_baseline_val:.3f})",
    )
    # 振幅を図示
    axs[1].annotate(
        "",
        xy=(t_out_min, out_baseline_val),
        xytext=(t_out_min, out_min_val),
        arrowprops=dict(arrowstyle="<->", color="brown", lw=1.5),
    )
    axs[1].text(
        t_out_min + (t_data_out.max() - t_data_out.min()) * 0.02,
        out_min_val + A_out / 2,
        f"A_out={A_out:.3f}",
        color="brown",
        va="center",
    )
elif not pd.isna(A_out) and A_out == 0:
    axs[1].hlines(
        out_max_val,
        t_data_out.min(),
        t_data_out.max(),
        colors="gray",
        linestyles="dashed",
        lw=1,
        label=f"Constant Value ({out_max_val:.3f})",
    )


axs[1].set_title(
    f"Output (out) Signal and Amplitude for ω = {target_omega_for_amplitude_plot}"
)
axs[1].set_xlabel("Time (t) [s]")
axs[1].set_ylabel("out Value")
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()
plt.show()
