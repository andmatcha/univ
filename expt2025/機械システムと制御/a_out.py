import pandas as pd
from pathlib import Path


data_path = Path(__file__).resolve().parent.joinpath("data/omega_phase_falling.csv")
df = pd.read_csv(data_path, header=0)
x = df["m"]

for n in x:
  print(n)
