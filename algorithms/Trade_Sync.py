from datetime import datetime
from decimal import Decimal

from algobaba.order_details import get_trade_price, get_trade_qty, order_status
from database.dao.client_dao import *
from utils.enums.signal import Signal
class TradeSync:
    def __init__(self,client_code):
        self.client_code = client_code
        self.db = self.get_database()
        
    def get_database(self):
    
        aws_access_key_id = 'AKIAW3MEAN3TBZIFTCE6'
        aws_secret_access_key = 'Ad2nS01Iioxl4cfqqDsXWBAoPd4SJRMqwdPpdFbj'

        # Create a DynamoDB resource object with your credentials
        dynamodb = boto3.resource(
            'dynamodb',
            region_name='ap-south-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)
        
        return dynamodb
    def verify_trades(self,orders):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for client in orders:
            client_orders = orders[client]
            for request_id,buy_stock in client_orders:
                order_execution_status = order_status(request_id)
                if(order_execution_status=="completed"):
                    trade_price = get_trade_price(request_id)
                    qty = get_trade_qty(request_id)
                    turnover = (qty*trade_price)
                    # TODO:- Do this once the trading order is placed
                    update_holding(self.db,self.client_code,buy_stock,qty,Decimal(trade_price),current_datetime)
                    add_trade_log(self.db,self.client_code,current_datetime,buy_stock,Signal.BUY.value,Decimal(trade_price),qty)
                    print(f"Stock: {buy_stock} Price_buy {trade_price} Quantity {qty}")
                    reduce_balance(self.db,self.client_code,Decimal(turnover))
                elif(order_execution_status=="SystemError"):
                    print("Shutdown all Systems")
                    break
                elif(order_execution_status=="rejected"):
                    print("Skip this client")
                    break
                    
                