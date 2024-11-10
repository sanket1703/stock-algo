class Order:
    def __init__(self, order_id, client_code, stock_code, quantity, limit_price, order_type, direction, status, message, exchange_trade_id, timestamp):
        self.order_id = order_id
        self.client_code = client_code
        self.stock_code = stock_code
        self.quantity = quantity
        self.limit_price = limit_price
        self.direction = direction
        self.order_type = order_type
        self.status = status
        self.message = message
        self.exchange_trade_id = exchange_trade_id
        self.timestamp = timestamp

    def to_json(self):
        return {
            "OrderID": self.order_id,
            "ClientCode": self.client_code,
            "StockCode": self.stock_code,
            "Quantity": round(self.quantity, 2),
            "LimitPrice": round(self.limit_price, 2),
            "Direction": self.direction,
            "Order Type": self.order_type,
            "Status": self.status,
            "Message": self.message,
            "ExchangeTradeID": self.exchange_trade_id,
            "Timestamp": self.timestamp
        }
