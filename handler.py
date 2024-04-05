from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm


def lambda_handler(event, context):
    stocks = [event['stock_list']]
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    mid_cap_algo.rank_stocks_by_ema_difference()
    print(mid_cap_algo.filter_stocks())
    print(mid_cap_algo.slot_fill())
    
    
if __name__ == "__main__":
    lambda_handler(None,None)