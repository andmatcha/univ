import networkx as nx
import time

# 駅間の所要時間データ
edges = [
    ("浅草", "田原町", 2, "銀座線"),
    ("田原町", "稲荷町", 1, "銀座線"),
    ("稲荷町", "上野", 2, "銀座線"),
    ("上野", "上野広小路", 1, "銀座線"),
    ("上野広小路", "末広町", 2, "銀座線"),
    ("末広町", "神田", 2, "銀座線"),
    ("神田", "三越前", 1, "銀座線"),
    ("三越前", "日本橋", 2, "銀座線"),
    ("日本橋", "京橋", 2, "銀座線"),
    ("京橋", "銀座", 1, "銀座線"),
    ("銀座", "新橋", 2, "銀座線"),
    ("新橋", "虎ノ門", 2, "銀座線"),
    ("虎ノ門", "溜池山王", 2, "銀座線"),
    ("溜池山王", "赤坂見附", 2, "銀座線"),
    ("赤坂見附", "青山一丁目", 2, "銀座線"),
    ("青山一丁目", "外苑前", 2, "銀座線"),
    ("外苑前", "表参道", 1, "銀座線"),
    ("表参道", "渋谷", 2, "銀座線"),
    ("池袋", "新大塚", 3, "丸ノ内線"),
    ("新大塚", "茗荷谷", 2, "丸ノ内線"),
    ("茗荷谷", "後楽園", 2, "丸ノ内線"),
    ("後楽園", "本郷三丁目", 2, "丸ノ内線"),
    ("本郷三丁目", "御茶ノ水", 2, "丸ノ内線"),
    ("御茶ノ水", "淡路町", 2, "丸ノ内線"),
    ("淡路町", "大手町", 2, "丸ノ内線"),
    ("大手町", "東京", 1, "丸ノ内線"),
    ("東京", "銀座", 3, "丸ノ内線"),
    ("銀座", "霞ケ関", 2, "丸ノ内線"),
    ("霞ケ関", "国会議事堂前", 2, "丸ノ内線"),
    ("国会議事堂前", "赤坂見附", 2, "丸ノ内線"),
    ("赤坂見附", "四ツ谷", 3, "丸ノ内線"),
    ("四ツ谷", "四谷三丁目", 2, "丸ノ内線"),
    ("四谷三丁目", "新宿御苑前", 2, "丸ノ内線"),
    ("新宿御苑前", "新宿三丁目", 2, "丸ノ内線"),
    ("新宿三丁目", "新宿", 1, "丸ノ内線"),
    ("新宿", "西新宿", 2, "丸ノ内線"),
    ("西新宿", "中野坂上", 2, "丸ノ内線"),
    ("中野坂上", "新中野", 2, "丸ノ内線"),
    ("新中野", "東高円寺", 2, "丸ノ内線"),
    ("東高円寺", "新高円寺", 2, "丸ノ内線"),
    ("新高円寺", "南阿佐ケ谷", 2, "丸ノ内線"),
    ("南阿佐ケ谷", "荻窪", 3, "丸ノ内線"),
    ("中野坂上", "中野新橋", 2, "丸ノ内線"),
    ("中野新橋", "中野富士見町", 2, "丸ノ内線"),
    ("中野富士見町", "方南町", 2, "丸ノ内線"),

]

# 無向グラフを作成
G = nx.Graph()

# エッジを追加
for u, v, weight, line in edges:
    G.add_edge(u, v, weight=weight, line=line)

# 出発地と目的地を指定
source = "渋谷"
target = "上野"

# 最短経路
time_start = time.perf_counter()  # 計測開始
shortest_path = nx.shortest_path(G, source=source, target=target, weight="weight")
time_end = time.perf_counter()  # 計測終了
# 所要時間
shortest_path_length = nx.shortest_path_length(
    G, source=source, target=target, weight="weight"
)

# 利用路線
current_line = G[shortest_path[0]][shortest_path[1]]["line"]
route_lines = [
    {
        "line": current_line,
        "from": shortest_path[0],
        "to": None,
        "station_count": None,
    }
]
station_count = 0  # 駅数
for i in range(1, len(shortest_path)):
    station_count += 1  # 駅数を足す
    current_station = shortest_path[i]  # 現在の駅
    if i == len(shortest_path) - 1:  # 目的駅の場合
        # 目的駅と駅数を反映
        route_lines[-1].update({"to": current_station, "station_count": station_count})
    else:  # 経由駅の場合
        next_station = shortest_path[i + 1]  # 次の駅
        next_line = G[current_station][next_station]["line"]  # 次の路線
        if current_line != next_line:  # 乗換が発生する場合
            # 最後の路線要素を更新
            route_lines[-1].update(
                {"to": current_station, "station_count": station_count}
            )
            # 新しく路線要素を追加
            route_lines.append(
                {
                    "line": next_line,
                    "from": current_station,
                    "to": None,
                    "station_count": None,
                }
            )
            current_line = next_line  # 現在の路線を更新
            station_count = 0  # 駅数をリセット

# 経路表示フォーマットを作成
formatted_route = f"{shortest_path[0]}"
for line in route_lines:
    formatted_route += f"--({line['line']} {line['station_count']}駅)-->{line['to']}"

# 経路と所要時間を表示
print("最短経路:", "".join(formatted_route))
print("所要時間: " + str(shortest_path_length) + "分")
print("実行時間:{:.5f}s".format((time_end - time_start)))
print(len(G.nodes()), len(G.edges()))
