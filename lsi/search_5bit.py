def analyze_alu_behavior(a_hex, b_hex, s_hex, y_hex):
    a = int(a_hex, 16) & 0x1F  # 5bit
    b = int(b_hex, 16) & 0x1F
    y = int(y_hex, 16) & 0x1F

    candidates = []

    # 算術
    if (a + b) & 0x1F == y:
        candidates.append("a + b")
    if (a - b) & 0x1F == y:
        candidates.append("a - b")
    if (b - a) & 0x1F == y:
        candidates.append("b - a")

    # ビット演算
    if (a & b) == y:
        candidates.append("a & b")
    if (a | b) == y:
        candidates.append("a | b")
    if (a ^ b) == y:
        candidates.append("a ^ b")
    if (~a & 0x1F) == y:
        candidates.append("~a")
    if (~b & 0x1F) == y:
        candidates.append("~b")
    if (a << 1) & 0x1F == y:
        candidates.append("a << 1")
    if (b << 1) & 0x1F == y:
        candidates.append("b << 1")
    if (a >> 1) == y:
        candidates.append("a >> 1")
    if (b >> 1) == y:
        candidates.append("b >> 1")
    if a == y:
        candidates.append("a")
    if b == y:
        candidates.append("b")

    # 比較
    if (1 if a == b else 0) == y:
        candidates.append("a == b")
    if (1 if a > b else 0) == y:
        candidates.append("a > b")
    if (1 if a < b else 0) == y:
        candidates.append("a < b")
    if abs(a - b) == y:
        candidates.append("|a - b|")

    return candidates


# 入力データ： [a, b, s, y]
data = [
    ["07", "03", "0", "0A"],
    ["03", "08", "1", "07"],
    ["15", "13", "2", "11"],
    ["01", "0C", "3", "13"],
    ["12", "05", "4", "17"],
    ["0A", "0A", "5", "01"],
    ["0F", "00", "6", "10"],
    ["00", "04", "7", "08"],
    ["19", "15", "8", "0C"],
    ["05", "0C", "9", "07"],
    ["06", "00", "A", "19"],
    ["09", "00", "B", "09"],
    ["19", "0A", "C", "00"],
    ["00", "15", "D", "15"],
    ["16", "00", "E", "0B"],
    ["12", "0D", "F", "01"],
]

print(f"{'s':<3} {'a':>2} {'b':>2} {'y':>2} | 推定される演算")
print("-" * 60)
for a_hex, b_hex, s_hex, y_hex in data:
    candidates = analyze_alu_behavior(a_hex, b_hex, s_hex, y_hex)
    result = ", ".join(candidates) if candidates else "不明"
    print(f"{s_hex:<3} {a_hex} {b_hex} {y_hex} | {result}")
