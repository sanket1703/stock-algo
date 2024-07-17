class Client:
    def __init__(self,client_code, current_balance,daily_trade_log,holding,brokerage):
        self.client_code = client_code
        self.current_balance = current_balance
        self.daily_trade_log = daily_trade_log
        self.holding = holding
        self.brokerage = brokerage

class DailyTradeLog:
    def __init__(self, date, stock_name, direction, price, qty,balance_before_trade):
        self.date = date
        self.stock_name = stock_name
        self.direction = direction
        self.price = price
        self.qty = qty
        self.balance_before_trade = balance_before_trade
    def to_list(self):
        return [self.date,self.stock_name,self.direction,self.price,self.qty,self.balance_before_trade]

class DailyOrderLog:
    def __init__(self, date, stock_name, direction, requestId, qty):
        self.date = date
        self.stock_name = stock_name
        self.direction = direction
        self.requestId = requestId
        self.qty = qty
    def to_list(self):
        return [self.date,self.stock_name,self.direction,self.requestId,self.qty]
     
class Holding:
    def __init__(self, stock_name, qty, last_buy_time_stamps, last_buy_price):
        self.stock_name = stock_name
        self.qty = qty
        self.last_buy_time_stamps = last_buy_time_stamps
        self.last_buy_price = last_buy_price
        
    def to_json(self):
        return {
            "stock_name" : self.stock_name,
            "qty" : self.qty,
            "last_buy_time_stamps" : self.last_buy_time_stamps,
            "last_buy_price" : self.last_buy_price
        }
