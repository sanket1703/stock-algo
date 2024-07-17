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