import pandas as pd
import statistics as stats

df = pd.read_csv("baseball_players.csv")
df_os = df[df["JPNorNot"] == "海外"]

# x:身長, y:体重
x = df_os["height"]
y = df_os["weight"]

# 1. x(身長)とy(体重)の平均値を計算
x_mean = stats.mean(x)
y_mean = stats.mean(y)

# 2. 回帰係数 (傾き) を計算
# 分子: Σ((x - x_mean) * (y - y_mean))
numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
# 分母: Σ((x - x_mean)^2)
denominator = sum((xi - x_mean) ** 2 for xi in x)
# 傾き
slope = numerator / denominator

# 3. 切片を計算
# 切片 = yの平均 - 傾き * xの平均
intercept = y_mean - slope * x_mean

# 4. 回帰式を出力
print(f"外国人選手の回帰式: y = {slope:.2f}x + {intercept:.2f}")
