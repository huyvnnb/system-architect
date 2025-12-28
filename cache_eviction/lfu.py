"""
LFU (Least Frequently Used)

GET(key):
    if key not in cache:
        return MISS
    increaseFreq(key)
    return value

PUT(key, value):
    if capacity == 0:
        return

    if key in cache:
        cache[key].value = value
        increaseFreq(key)
    else:
        if size == capacity:
            evictKey = freqMap[minFreq].removeOldest()
            delete cache[evictKey]
        cache[key] = (value, freq=1)
        freqMap[1].add(key)
        minFreq = 1

increaseFreq(key):
    freq = cache[key].freq
    freqMap[freq].remove(key)
    if freqMap[freq] empty and freq == minFreq:
        minFreq += 1
    cache[key].freq += 1
    freqMap[freq + 1].add(key)
"""
from collections import OrderedDict, defaultdict
from typing import Dict, Tuple, List


class LFU:
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.size: int = 0
        self.key_map: Dict[int, List[int]] = {}  # key -> (value, freq)
        self.freq_map = defaultdict(OrderedDict)  # freq -> OrderedDict()
        self.min_freq: int = 0

    def get(self, key):
        if key not in self.key_map:
            return None

        self._increase_freq(key)
        return self.key_map[key][0]  # value

    def put(self, key, value):
        if self.capacity == 0:
            return

        if key in self.key_map:
            self.key_map[key][0] = value  # set new value for key
            self._increase_freq(key)

        else:
            if self.size == self.capacity:
                evict_key, _ = self.freq_map[self.min_freq].popitem(last=False)
                del self.key_map[evict_key]
                self.size -= 1

            self.key_map[key] = [value, 1]
            self.freq_map[1][key] = None
            self.min_freq = 1
            self.size += 1

    def _increase_freq(self, key: int):
        _, freq = self.key_map[key]
        del self.freq_map[freq][key]

        if not self.freq_map[freq] and freq == self.min_freq:  # if key is empty -> update min_freq
            self.min_freq += 1

        self.key_map[key][1] += 1
        self.freq_map[freq + 1][key] = None  # add new freq map {freq: 2 -> {{1:None}, {2:None}}


if __name__ == '__main__':
    lfu = LFU(capacity=3)

    lfu.put(1, 1)
    lfu.put(2, 2)

    print(lfu.get(1))
    lfu.get(2)

    lfu.put(3, 3)
    lfu.get(3)
    lfu.get(3)
    for key, val in lfu.key_map.items():
        print(key, val)

    for key, val in lfu.freq_map.items():
        print(key, val)


