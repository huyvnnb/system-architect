"""
Counting Bloom Filter

Initialize:
    m = size of counter array
    k = number of hash functions
    counter_array = [0] * m

Add(key):
    for i in 1..k:
        index = hash_i(key) % m
        counter_array[index] += 1

Remove(key):
    for i in 1..k:
        index = hash_i(key) % m
        if counter_array[index] > 0:
            counter_array[index] -= 1

Check(key):
    for i in 1..k:
        index = hash_i(key) % m
        if counter_array[index] == 0:
            return False   // chắc chắn không tồn tại
    return True            // có thể tồn tại

"""
import mmh3


class CountingBloomFilter:
    def __init__(self, size: int, hash_count: int):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def _hashes(self, key: str):
        for seed in range(self.hash_count):
            yield mmh3.hash(key, seed) % self.size

    def add(self, key: str):
        for index in self._hashes(key):
            self.bit_array[index] += 1

    def remove(self, key: str):
        for index in self._hashes(key):
            if self.bit_array[index] > 0:
                self.bit_array[index] -= 1

    def check(self, key: str) -> bool:
        for index in self._hashes(key):
            if self.bit_array[index] == 0:
                return False
        return True


if __name__ == '__main__':
    bf = CountingBloomFilter(size=10000, hash_count=5)

    bf.add("user:1")
    bf.add("user:2")
    bf.add("user:3")

    print(bf.check("user:1"))  # True
    print(bf.check("user:2"))
    print(bf.check("user:3"))

    bf.remove("user:4")
    bf.remove("user:3")
    print(bf.check("user:3"))