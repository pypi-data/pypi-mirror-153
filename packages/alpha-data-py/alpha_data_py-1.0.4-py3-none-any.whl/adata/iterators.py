import time


class BaseIterator:
    def __init__(self, q):
        self.q = q

    def close(self):
        self.q.close()

    def err(self):
        return self.q.err()


class FloatIterator(BaseIterator):
    def __init__(self, q, time=0, float=0.0):
        super().__init__(q)
        self.time = time
        self.float = float

    def next(self):
        ok = self.q.next()
        if not ok:
            return False
        tick, obj, _ = self.q.read()
        self.float = obj.value
        self.time = tick
        return True


class TradeIterator(BaseIterator):
    def __init__(self, q, time=0, price=0.0, size=0.0):
        super().__init__(q)
        self.time = time
        self.price = price
        self.size = size

    def next(self):
        ok = self.q.next()
        if not ok:
            return False
        tick, obj, _ = self.q.read()
        self.time = tick
        self.price = obj.price()
        self.size = obj.size()
        return True


class OHLCVIterator(BaseIterator):
    def __init__(self, q, time=0, o=0.0, h=0.0, l=0.0, c=0.0,
                 buy_count=0, sell_count=0, buy_vol=0.0, sell_vol=0.0, price=0.0):
        super().__init__(q)
        self.time = time
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        self.buy_count = buy_count
        self.sell_count = sell_count
        self.buy_vol = buy_vol
        self.sell_vol = sell_vol
        self.price = price

    def next(self):
        ok = self.q.next()
        if not ok:
            return False
        tick, obj, _ = self.q.read()
        self.time = tick
        self.o = obj.o
        self.h = obj.h
        self.l = obj.l
        self.c = obj.c
        self.buy_count = obj.buy_count
        self.sell_count = obj.sell_count
        self.buy_vol = obj.buy_vol
        self.sell_vol = obj.sell_vol
        self.price = obj.price
        return True


class LiquidityIterator(BaseIterator):
    def __init__(self, q, time=0, map=None, ts=0.0):
        super().__init__(q)
        if map is None:
            map = {}
        self.time = time
        self.map = map
        self.ts = ts

    def next(self):
        ok = self.q.next()
        if not ok:
            return False
        tick, obj, _ = self.q.read()
        self.time = tick
        self.map = obj.map
        self.ts = obj.ts
        return True
