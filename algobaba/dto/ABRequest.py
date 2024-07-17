import json

class ABOrderRequest:
    def __init__(self,SourceSymbol, TransactionType,StrategyTag,Quantity):
        self.SourceSymbol = SourceSymbol
        self.TransactionType = TransactionType
        self.StrategyTag = StrategyTag
        self.Quantity = Quantity

    def to_dict(self):
        return {
            'SourceSymbol': self.SourceSymbol,
            'TransactionType': self.TransactionType,
            'StrategyTag': self.StrategyTag,
            'Quantity': self.Quantity
        }

class ABOrderStatusRequest:
    def __init__(self,request_id):
        self.request_id = request_id
        
    def to_dict(self):
        return {
            'RequestId': self.request_id
        }