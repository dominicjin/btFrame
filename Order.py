class Order:
    # static id
    order_id = 0

    def __init__(self, orderType, asset, quantity=None, price=None):
        self.orderType = orderType
        self.quantity = quantity
        self.status = 'pending'
        self.price = price
        self.asset = asset
        # self.submitTime = time
        # self.executeTime = None
        self.order_id += 1
    
    def orderInfo(self):
        return {
            "orderId": Order.order_id,
            "orderType": self.orderType,
            "quantity": self.quantity,
            "price" : self.price,
            "asset" : self.asset,
            "status": self.status,
            # "submitTime": self.submitTime,
            # "executeTime": self.executeTime
        }
    
