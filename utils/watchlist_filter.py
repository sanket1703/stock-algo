def massage_watchlist(watchlist):

    temp = []

    for stock in watchlist:
        stock += ".NS"
        temp.append(stock)
    
    return temp
