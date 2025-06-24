# 積分器のゲインと位相
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

#### -------- データ -------- ####
# 条件A 実験値
df_a = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_a.csv"), header=0
)
# 条件B 実験値
df_b = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_b.csv"), header=0
)
# 条件C 実験値
df_c = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_c.csv"), header=0
)
# ゲイン理論値
df_theoretical_gain = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_theoretical_gain.csv"),
    header=0,
)
# 位相理論値
df_theoretical_gain = pd.read_csv(
    Path(__file__).resolve().parent.joinpath("data/sekibunki_theoretical_phase.csv"),
    header=0,
)


