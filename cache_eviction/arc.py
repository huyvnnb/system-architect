"""
ARC (Adaptive Replacement Cache)  --> Waiting for implementation

GET(key):
    if key in T1 or T2:
        move key to T2
        return HIT

    if key in B1:
        p = min(p + delta, capacity)
        replace()
        move key to T2
        return HIT

    if key in B2:
        p = max(p - delta, 0)
        replace()
        move key to T2
        return HIT

    replace()
    insert key into T1

REPLACE():
    if size(T1) > p:
        move LRU(T1) to B1
    else:
        move LRU(T2) to B2
"""