from typing import Any, List

import mmh3

from sortedcontainers import SortedDict


class Node:
    def __init__(self, host: str, port: int, weight: int = 1):
        self.id = f"{host}:{port}"
        self.weight = weight
        self.data = {}


class VNode:
    def __init__(self, hash_value: int, node: "Node"):
        self.hash = hash_value
        self.node = node


class Rebalancer:
    def __init__(self, ring: "ConsistentHash"):
        self.ring = ring

    def on_node_added(self, new_node: Node):
        for vnode in self.ring.get_vnodes(new_node):
            prev = self.ring.prev_node(vnode.hash)
            print(
                f"Migrate keys in range "
                f"({prev.hash}, {vnode.hash}] "
                f"from {prev.node.id} → {new_node.id}"
            )

    def on_node_removed(self, node: Node):
        print(f"All keys of {node.id} must be reassigned")


class ConsistentHash:
    def __init__(self, replicas: int):
        self.replicas = replicas
        self.hash_ring = SortedDict() # hash -> VNode

    def add_node(self, node: Node):
        for i in range(self.replicas * node.weight):
            vnode_key = f"{node.id}#{i}"
            h = key_hash(vnode_key)
            self.hash_ring[h] = VNode(h, node)

    def remove_node(self, node: Node):
        to_remove = []
        for h, vnode in self.hash_ring.items():
            if vnode.node == node:
                to_remove.append(h)

        for h in to_remove:
            del self.hash_ring[h]

    def find_node(self, key: Any):
        if not self.hash_ring:
            return None

        h = key_hash(key)
        idx = self.hash_ring.bisect_left(h)

        if idx == len(self.hash_ring):
            idx = 0

        return self.hash_ring.values()[idx].node

    def prev_node(self, h: int):
        idx = self.hash_ring.bisect_left(h)

        if idx == 0:
            idx = len(self.hash_ring)

        return self.hash_ring.values()[idx - 1]

    def get_vnodes(self, node: Node) -> List[VNode]:
        return [v for v in self.hash_ring.values() if v.node == node]


def key_hash(key: Any) -> int:
    if not isinstance(key, str):
        key = str(key)
    return mmh3.hash(key, seed=0) & 0xffffffff


if __name__ == '__main__':
    engine = ConsistentHash(replicas=3)
    rebalancer = Rebalancer(engine)

    n1 = Node("192.168.1.1", 3030)
    n2 = Node("192.168.1.2", 8080)
    n3 = Node("192.168.1.3", 9000)

    engine.add_node(n1)
    engine.add_node(n2)

    engine.add_node(n3)
    rebalancer.on_node_added(n3)

    engine.remove_node(n1)
    rebalancer.on_node_removed(n1)


