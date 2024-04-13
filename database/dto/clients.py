class Client:
    def __init__(self,client_code, current_balance,daily_trade_log,holding):
        self.client_code = client_code
        self.current_balance = current_balance
        self.daily_trade_log = daily_trade_log
        self.holding = holding

class DailyTradeLog:
    def __init__(self, date, stock_name, direction, price, charges, net, balance):
        self.date = date
        self.stock_name = stock_name
        self.direction = direction
        self.price = price
        self.charges = charges
        self.net = net
        self.balance = balance
     
class Holding:
    def __init__(self, stock_name, qty, last_buy_time_stamps, last_buy_price):
        self.stock_name = stock_name
        self.qty = qty
        self.last_buy_time_stamps = last_buy_time_stamps
        self.last_buy_price = last_buy_price
