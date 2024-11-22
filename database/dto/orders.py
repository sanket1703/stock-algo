class Order:
    def __init__(self, order_id, client_code, stock_code, status, exchange_trade_id, quantity, qty_traded, limit_price, trade_price, order_type, message, direction, sync_status, timestamp):
        self.order_id = order_id
        self.client_code = client_code
        self.stock_code = stock_code
        self.status = status
        self.exchange_trade_id = exchange_trade_id
        self.quantity = quantity
        self.qty_traded = qty_traded
        self.limit_price = limit_price
        self.trade_price = trade_price
        self.order_type = order_type
        self.message = message
        self.direction = direction
        self.sync_status = sync_status
        self.timestamp = timestamp

    def to_json(self):
        return {
            "OrderID": self.order_id,
            "ClientCode": self.client_code,
            "StockCode": self.stock_code,
            "Direction": self.direction,
            "Status": self.status,
            "Quantity": round(self.quantity, 2),
            "QtyTraded": round(self.qty_traded, 2),
            "LimitPrice": round(self.limit_price, 2),
            "TradePrice": round(self.trade_price, 2),
            "Order Type": self.order_type,
            "Message": self.message,
            "ExchangeTradeID": self.exchange_trade_id,
            "Timestamp": self.timestamp,
            "SyncStatus": self.sync_status
        }
