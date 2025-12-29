# Write-through
```
function write_through(address, value):
    cache[address] = value      // ghi vào cache
    RAM[address] = value        // ghi đồng thời vào bộ nhớ chính
```
- Đơn giản, dữ liệu luôn đồng bộ RAM.

# Write-back
```
function write_back(address, value):
    cache[address] = value          // ghi vào cache
    cache.mark_dirty(address)       // đánh dấu cache là dirty

function evict_from_cache(address):
    if cache.is_dirty(address):
        RAM[address] = cache[address]  // đẩy dữ liệu dirty vào RAM
    cache.remove(address)
```

Đặc điểm: dữ liệu trong RAM không đồng bộ ngay, chỉ khi cache bị đẩy ra.

# Write-around
```
function write_around(address, value):
    RAM[address] = value       // ghi thẳng vào RAM, không cập nhật cache

function read(address):
    if cache.contains(address):
        return cache[address]
    else:
        value = RAM[address]  // lấy từ RAM
        cache[address] = value
        return value
```
