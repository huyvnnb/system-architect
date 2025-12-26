"""
Bloom Filter (không cho xóa)

Initialize:
    m = size of bit array
    bit_array = [0] * m
    k = number of hash functions

    m = -(n * ln(p)) / (ln(2)^2)
    k = (m / n) * ln(2)

Add(element):
    for i in 1..k:
        index = hash_i(element) % m
        bit_array[index] = 1

Check(element):
    for i in 1..k:
        index = hash_i(element) % m
        if bit_array[index] == 0:
            return False   // chắc chắn không tồn tại
    return True            // có thể tồn tại


Initialize:
    bloom_filter = new BloomFilter()
    cache = new Cache()      // ví dụ Redis
    database = Database()

// Khởi tạo Bloom Filter với các key "có thể tồn tại"
for key in database.getAllKeys():
    bloom_filter.Add(key)

Function getValue(key):
    // Bước 1: Kiểm tra Bloom Filter
    if not bloom_filter.Check(key):
        return NULL   // chắc chắn key không tồn tại → không truy cập DB

    // Bước 2: Kiểm tra cache
    value = cache.get(key)
    if value is not NULL:
        return value

    // Bước 3: Truy vấn DB nếu Bloom Filter báo "có thể tồn tại"
    value = database.query(key)
    if value is not NULL:
        cache.set(key, value)    // lưu vào cache để lần sau không query DB
    return value
"""
import mmh3


class BloomFilter:
    def __init__(self, size: int, hash_count: int):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [0] * size

    def _hashes(self, key: str):
        for seed in range(self.hash_count):
            yield mmh3.hash(key, seed) % self.size

    def add(self, key: str):
        for index in self._hashes(key):
            self.bit_array[index] = 1

    def check(self, key: str) -> bool:
        for index in self._hashes(key):
            if self.bit_array[index] == 0:
                return False
        return True


if __name__ == '__main__':
    bf = BloomFilter(size=10000, hash_count=5)

    bf.add("user:1")
    bf.add("user:2")

    print(bf.check("user:1"))  # True
    print(bf.check("user:2"))
    print(bf.check("user:3"))
