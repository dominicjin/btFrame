class Position:
    def __init__(self, asset, price, size):
        self.asset = asset
        self.size = size  # 正数表示多仓，负数表示空仓
        self.price = price

    def long_position(self, price, size):
        """开多仓或增加多仓"""
        self.size += size
        self.price = price 

    def short_position(self, price, size):
        """开空仓或增加空仓"""
        self.size -= size
        self.price = price

    def update_price(self, price):
        self.price = price

    @property
    def value(self):
        return self.size * self.price

    @property
    def is_long(self):
        return self.size > 0

    @property
    def is_short(self):
        return self.size < 0
