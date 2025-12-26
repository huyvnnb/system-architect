"""
HyperLogLog

Initialize:
    p = number of bits for bucket index
    m = 2^p                     // số bucket (register)
    registers = [0] * m         // mỗi register lưu max số leading-zero

Add(x):
    h = hash(x)                 // hash ngẫu nhiên (bit string)

    bucket = first p bits of h
    remaining_bits = h[p:]

    rho = count_leading_zeros(remaining_bits) + 1

    registers[bucket] = max(registers[bucket], rho)

Estimate():
    sum = 0
    for r in registers:
        sum += 2^(-r)

    Z = 1 / sum                 // harmonic mean

    estimate = alpha * m^2 * Z
    return estimate

Merge(hll1, hll2):
    for i in 0..m-1:
        hll1.registers[i] = max(hll1.registers[i], hll2.registers[i])
"""
import math

import mmh3


class HLL:
    def __init__(self, p: int = 12):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()

    def _get_alpha(self):
        if self.m == 16:
            return 0.673
        elif self.m == 32:
            return 0.697
        elif self.m == 64:
            return 0.709
        else:
            return 0.7213 / (1 + 1.079 / self.m)

    def _hashes(self, key: str):
        return mmh3.hash64(key, signed=False)[0]

    @staticmethod
    def _leading_zeros(x: int, bits: int):
        if x == 0:
            return bits
        return bits - x.bit_length()

    def add(self, key: str):
        h = self._hashes(key)

        # first p bits
        bucket = h >> (64 - self.p)
        remaining = h & ((1 << (64 - self.p)) - 1)

        rho = self._leading_zeros(remaining, 64 - self.p) + 1
        self.registers[bucket] = max(rho, self.registers[bucket])

    def estimate(self) -> int:
        indicator_sum = 0.0
        for r in self.registers:
            indicator_sum += 2 ** (-r)

        raw_estimate = self.alpha * (self.m ** 2) / indicator_sum
        zeros = self.registers.count(0)

        if raw_estimate <= 2.5 * self.m and zeros > 0:
            return int(self.m * math.log(self.m / zeros))

        return int(raw_estimate)

    def merge(self, other: "HLL"):
        if self.p != other.p:
            raise ValueError("Cannot merge HLL with different p")

        for i in range(self.m):
            self.registers[i] = max(self.registers[i], other.registers[i])


if __name__ == '__main__':
    hll = HLL(p=12)

    for i in range(1, 10000):
        hll.add(f"user_{i}")

    print("Estimated unique users:", hll.estimate())

    hll1 = HLL()
    hll2 = HLL()

    for i in range(1, 50_001):
        hll1.add(f"user_{i}")

    for i in range(25_001, 100_001):
        hll2.add(f"user_{i}")

    hll1.merge(hll2)

    print(hll1.estimate())
