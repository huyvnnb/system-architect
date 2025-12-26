"""
Count-Min Sketch (CMS)

d rows (hash functions)
w columns (counter per row)

matrix[d][w]

Initialize:
    d = number of hash functions
    w = number of buckets per hash
    table[d][w] = 0              // ma trận counter

Add(x):
    for i = 1 to d:
        idx = hash_i(x) mod w
        table[i][idx] += 1

Query(x):
    min_count = +∞
    for i = 1 to d:
        idx = hash_i(x) mod w
        min_count = min(min_count, table[i][idx])
    return min_count


Merge(CMS_A, CMS_B):
    for i = 1 to d:
        for j = 1 to w:
            CMS_A.table[i][j] += CMS_B.table[i][j]
"""
import math

import mmh3


class CMS:
    def __init__(self, epsilon: float = 0.01, delta: float = 0.001):
        self.w = math.ceil(math.e / epsilon)  # number of buckets
        self.d = math.ceil(math.log(1 / delta))  # number of hash functions

        self.table = [[0] * self.w for _ in range(self.d)]

    def _hashes(self, key: str, seed: int) -> int:
        return mmh3.hash(key, seed, signed=False) % self.w

    def add(self, key: str, count: int = 1):
        for i in range(self.d):
            h = self._hashes(key, i)
            self.table[i][h] += count

    def estimate(self, key: str):
        min_count = float("inf")
        for i in range(self.d):
            idx = self._hashes(key, i)
            min_count = min(min_count, self.table[i][idx])

        return min_count

    def merge(self, other: "CMS"):
        if self.w != other.w or self.d != other.d:
            raise ValueError("Cannot merge two CMS with different parameters")

        for i in range(self.d):
            for j in range(self.w):
                self.table[i][j] += other.table[i][j]


if __name__ == "__main__":
    cms = CMS(epsilon=0.01, delta=0.001)

    # giả lập traffic
    for _ in range(100_000):
        cms.add("api:/login")

    for _ in range(5_000):
        cms.add("api:/health")

    print("login:", cms.estimate("api:/login"))
    print("health:", cms.estimate("api:/health"))

