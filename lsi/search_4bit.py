def alu_operations(a: int, b: int, expected_y: int) -> list:
    a4 = a & 0xF
    b4 = b & 0xF
    y4 = expected_y & 0xF

    candidates = []

    # 基本演算
    if (a4 + b4) & 0xF == y4:
        candidates.append("a + b")
    if (a4 - b4) & 0xF == y4:
        candidates.append("a - b")
    if (b4 - a4) & 0xF == y4:
        candidates.append("b - a")
    if (a4 & b4) == y4:
        candidates.append("a & b")
    if (a4 | b4) == y4:
        candidates.append("a | b")
    if (a4 ^ b4) == y4:
        candidates.append("a ^ b")
    if (~a4 & 0xF) == y4:
        candidates.append("~a")
    if (~b4 & 0xF) == y4:
        candidates.append("~b")
    if (a4 << 1) & 0xF == y4:
        candidates.append("a << 1")
    if (a4 >> 1) == y4:
        candidates.append("a >> 1")
    if b4 == y4:
        candidates.append("b")
    if a4 == y4:
        candidates.append("a")
    if (a4 & ~b4 & 0xF) == y4:
        candidates.append("a & ~b")

    return candidates

# テストベンチのデータ
test_vectors = [
    (8, 6, 6),
    (6, 10, 12),
    (9, 3, 11),
    (12, 7, 5),
    (3, 0, 3),
    (10, 15, 0),
    (12, 6, 4),
    (7, 2, 9)
]

print(f"{'Index':<5} {'a':>2} {'b':>2} {'y':>2} | Matching Operations")
print("-" * 50)
for idx, (a, b, y) in enumerate(test_vectors):
    ops = alu_operations(a, b, y)
    op_str = ', '.join(ops) if ops else "なし"
    print(f"{idx+1:<5} {a:>2} {b:>2} {y:>2} | {op_str}")
