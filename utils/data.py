def get_s_data():
     
    n=4
    startdate=datetime.now()-timedelta(days=n)
    enddate=datetime.now()

    sd=startdate.strftime("%Y-%m-%d")
    ed=enddate.strftime("%Y-%m-%d")
    data=pd.DataFrame
    data = {"symbol":'NSE:NIFTY50-INDEX',"resolution":"1","date_format":"1","range_from":sd,"range_to":ed,"cont_flag":"1"}
    x1=fyers.history(data)
    hist_data=pd.DataFrame(x1['candles'])
    hist_data[0]=pd.to_datetime(hist_data[0],unit='s')


    hist_data[0]=hist_data[0].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')

    hist_data[0]=hist_data[0].dt.tz_localize(None)

    hist_data=hist_data.set_index(0)

    #Date,Open,High,Low,Close,Adj Close,Volume

    hist_data.rename(columns={0: '0', 1: 'open',2: 'high',3: 'low',4: 'close',5:'volume'}, inplace=True)
    hist_data.to_csv(f'./nifty50_1m.csv')