"""
Highest Random Weight (HRW) hashing

weight(key, node) = hash(key, node) * node_weight

Input:
  keys = [k1, k2, ..., kn]
  nodes = [n1, n2, ..., nm]
  node_weights = { n1: w1, n2: w2, ..., nm: wm }  // optional

Function get_node_for_key(key, nodes, node_weights):
    max_weight = -∞
    selected_node = None

    for node in nodes:
        // Tạo hash kết hợp key và node
        hash_value = hash(key + node)
        weight = hash_value * node_weights.get(node, 1)  // nếu không có weight mặc định là 1

        if weight > max_weight:
            max_weight = weight
            selected_node = node

    return selected_node
"""
from typing import List

import mmh3


class Node:
    def __init__(self, host: str, port: int, weight: int = 1):
        self.id = f"{host}:{port}"
        self.weight = weight
        self.data = {}


class RendezvousHash:
    def __init__(self):
        self.nodes: List["Node"] = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def remove_node(self, node_id: str):
        self.nodes = [n for n in self.nodes if n.id != node_id]

    def get_node(self, key: str):
        max_score = -1
        selected_node = None
        for node in self.nodes:
            score = _hash(key, node.id)
            if score > max_score:
                max_score = score
                selected_node = node

        return selected_node


def _hash(key: str, node_id: str) -> int:
    data = f"{key}-{node_id}".encode("utf-8")
    h = mmh3.hash(data, seed=0, signed=False)
    return h


if __name__ == '__main__':
    rh = RendezvousHash()

    n1 = Node("192.168.1.1", 3030)
    n2 = Node("192.168.1.2", 8080)
    n3 = Node("192.168.1.3", 9000)

    rh.add_node(n1)
    rh.add_node(n2)
    rh.add_node(n3)

    keys = ["user1", "user2", "user3", "user4"]
    for k in keys:
        node = rh.get_node(k)
        print(f"Key {k} được gán cho node {node.id}")

    rh.remove_node(n1.id)
    print("\nSau khi xóa node N1:")
    for k in keys:
        node = rh.get_node(k)
        print(f"Key {k} được gán cho node {node.id}")