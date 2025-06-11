class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        # Nodeクラスのインスタンスを文字列表現にする
        left = f"[{self.left.value}]" if self.left else "[]"
        right = f"[{self.right.value}]" if self.right else "[]"
        return f"{left} <- {self.value} -> {right}"


class BinarySearchTree:

    def __init__(self):
        self.nodes = []

    def add_node(self, value):
        node = Node(value)
        if self.nodes:
            # 自分の親ノードを探す
            parent, direction = self.find_parent(value)
            if direction == "left":
                parent.left = node
            else:
                parent.right = node
        # この木のノードとして格納
        self.nodes.append(node)

    def find_parent(self, value):
        node = self.nodes[0]
        # nodeがNoneになるまでループを回す
        while node:
            p = node  # 戻り値の候補（親かもしれない）としてとっておく。
            if p.value == value:
                raise ValueError("すでにある値と同じ値を格納することはできません。")
            if p.value > value:
                direction = "left"
                node = p.left
            else:
                direction = "right"
                node = p.right
        return p, direction


# 乱数を生成
import random
data = random.sample(range(1, 100), 10)
print(data)

# 二分探索木を作成
bst = BinarySearchTree()
for i in data:
    bst.add_node(i)

# 二分探索木を表示
for i in bst.nodes:
    print(i)
