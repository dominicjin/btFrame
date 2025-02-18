class Position:
    def __init__(self, asset, price, size):
        self.position = False
        self.asset = asset
        self.size = size
        self.price = price

    def long_position(self, price, size):
        self.size += size
        self.price = price 

    def short_position(self, price, size):
        self.size -= size
        self.price = price

    def update_price(self, price):
        self.price = price

    @property
    def value(self):
        return self.size * self.price
