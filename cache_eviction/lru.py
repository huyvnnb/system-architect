"""
LRU (Least Recently Used)

GET(key):
    if key not in map:
        return MISS
    node = map[key]
    move_to_head(node)
    return node.value

PUT(key, value):
    if key in map:
        node = map[key]
        node.value = value
        move_to_head(node)
    else:
        if size == capacity:
            evict = tail
            remove(evict)
            delete map[evict.key]
        node = new Node(key, value)
        add_to_head(node)
        map[key] = node
"""
from collections import OrderedDict


class LRU:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1

        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int):
        if key in self.cache:
            self.cache.move_to_end(key)

        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


if __name__ == '__main__':
    lru = LRU(capacity=1)
    lru.put(1, 1)
    lru.put(2, 2)

    print(lru.get(1))
    lru.put(3, 3)
    print(lru.get(3))