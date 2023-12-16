import pandas as pd

def BUY_EXE(pivot,lot): 
    
    #TODO:- Handle these data points
 
    global dfx
    global data
    global tl_df
    global SLP
    global TP
    global EP
    global SIDE
    global riskdf
    global SR_QTY
    global OPX_TOKEN
    global TRIGGER
    global LIMIT
    global OPXDF
    global MODE
    
    
    data = pd.read_csv(f'./nifty50_1m.csv')
    data['time']=pd.to_datetime(data['0'])
    dfx=data.set_index(["time"])
    dfx=dfx.between_time('9:15',"15:30")
    dfx.index=pd.to_datetime(dfx.index)
    dfx['atr']=atr_ind(dfx,14)
    dfx=dfx.dropna()
    s="NIFTY50"
    
    q=dfx.iloc[-5]
    u=dfx.iloc[-4]
    o=dfx.iloc[-3]
    p=dfx.iloc[-2]
    a=dfx.iloc[-1]
    
    now = datetime.now().strftime("%H:%M:%S")
    RR=3
    risk=riskdf[-1]
    print('risk= ',risk)
    
    

    
   
    
    ########################################################  ENTRY LOGIC  #################################################
    
    if  now > starttime   and now < endtime and tl_df[-1] == 0 :
        print (f"LOOKING FOR NEW TRADES..at {pivot} ")
        print(datetime.now().strftime("%H:%M:%S:%f"),f"------------- atr ={p['atr']}_____________ltp= {dfx.iloc[-1]['close']}")
        print(f'                    ltp=',a['close'],'                                     ')
        print('                                                         ')        
                                       ######################    BUY CALL OPX  #########################

        if q['low']> pivot and u['low']> pivot and o['open'] > pivot and o['close'] > pivot  and o['close']< o['open'] and  p['close']>o['open'] and o['low'] < pivot and abs(  max(  float(p['close'])-float(p['open']),float(p['close'])-float(o['close'] ))) >= (p['atr']/2): 
            
            print('                                                         ')
            print('                        _______BE with 1/2 ATR_______                                 ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ' ,min(p['low'],o['low']) ,'Entry= ' , p['close']       )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=CE_token_with_vol(latm,hatm)
            lastval= max(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"c")
            risk=risk*factor
            print('delta = ',1/factor)
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(   float(lastval) -  min(  float(p['low']),float(o['low'])  ))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)
            #------------------------------------

            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')


            stop_entry_logic()
            
            RR=float(RR)
            takeprofit=float(lastval+(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=min(p['low'],o['low'])
            stoplossprice=float(stoplossprice)
            cepe= "ce"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)


            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
    
            
        elif q['low']> pivot and u['low']> pivot and o['open'] > pivot and o['close'] > pivot  and   o['low'] < pivot and p['open'] < p['close'] and abs( max( float(p['close'])-float(p['open']) ,float (p['close'])-float(o['close']) ) ) >= (p['atr']) :
            
            print('                __________bounce > ATR___________                                         ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ' ,min(p['low'],o['low']) ,'Entry= ' , p['close']       )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=CE_token_with_vol(latm,hatm)
            lastval= max(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"c")
            risk=risk*factor
            print('delta = ',1/factor)
               
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(   float(lastval) -  min(  float(p['low']),float(o['low'])  ))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)
            #------------------------------------

            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')


            stop_entry_logic()
            
            RR=float(RR)
            takeprofit=float(lastval+(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=min(p['low'],o['low'])
            stoplossprice=float(stoplossprice)
            cepe= "ce"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)


            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
    

        
        elif q['low']> pivot and u['low']> pivot and o['open'] > pivot and o['close'] > pivot and o['low'] < pivot  and  p['close']> u['open'] and o['close']< o['open'] and u['close']< u['open'] and  abs(   max(   float(p['close']) - float(p['open']) ,float (P['close']) -float(o['close'])  )) >= (p['atr']/2) : 
            
            print('                        __________double BE with 1/2 ATR______                                 ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ' ,min(p['low'],o['low']) ,'Entry= ' , p['close']       )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=CE_token_with_vol(latm,hatm)
            lastval= max(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"c")
            risk=risk*factor
            print('delta = ',1/factor)
               
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(   float(lastval) -  min(  float(p['low']),float(o['low'])  ))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)
            #------------------------------------

            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')


            stop_entry_logic()
            
            RR=float(RR)
            takeprofit=float(lastval+(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=min(p['low'],o['low'])
            stoplossprice=float(stoplossprice)
            cepe= "ce"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)


            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
    

            
        elif  q['low']> pivot and u['low']> pivot and  o['low'] > pivot  and p['low'] < pivot and p['close'] > o['open']  and o['open'] > o['close']  :  
           
            print('                     ______BE PINBAR____                                    ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ' ,min(p['low'],o['low']) ,'Entry= ' , p['close']       )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=CE_token_with_vol(latm,hatm)
            lastval= max(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"c")
            risk=risk*factor
            print('delta = ',1/factor)
               
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(   float(lastval) -  min(  float(p['low']),float(o['low'])  ))
            qty=  lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)
            #------------------------------------

            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')


            stop_entry_logic()
            
            RR=float(RR)
            takeprofit=float(lastval+(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=min(p['low'],o['low'])
            stoplossprice=float(stoplossprice)
            cepe= "ce"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)


            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
    
                        

        elif q['low']> pivot and u['low']> pivot and o['open'] > pivot and o['close'] > pivot  and   o['low'] < pivot and p['open'] < p['close'] and p['close'] > q['open'] and  q['close']< q['open'] and u['close']< u['open']  and abs( max( float(p['close'])-float(p['open']) ,float (p['close'])-float(o['close']) ) ) >= (p['atr']/2) :
            
            print('                __________bounce = triple BE 1/2 atr ___________                                         ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ' ,min(p['low'],o['low']) ,'Entry= ' , p['close']       )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=CE_token_with_vol(latm,hatm)
            lastval= max(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"c")
            risk=risk*factor
            print('delta = ',1/factor)
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(   float(lastval) -  min(  float(p['low']),float(o['low'])  ))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)
            #------------------------------------

            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')


            stop_entry_logic()
            
            RR=float(RR)
            takeprofit=float(lastval+(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=min(p['low'],o['low'])
            stoplossprice=float(stoplossprice)
            cepe= "ce"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)


            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
    

        



            #########################################      DONE       ####################################################
            
    elif now < starttime and now > "05:10:10":
        print(f"WAITING FOR{starttime} .......")
        print ("NEW DAY NEW MONEY TO BE MADE.....")
        print(datetime.now().strftime("%H:%M:%S") )
  
        
        
    elif now > endtime:
        print(now)
        print(f"NO NEW TRADES AFTER {endtime}")
        print ("WARS DON'T END WHEN YOU LOSE..... WARS ARE ONLY LOST WHEN ONE GIVES UP")
        
        
        
    else:
        print(datetime.now().strftime("%H:%M:%S"),'trade taken' )

def SELL_EXE(pivot,lot):
    #stock1_pre_exe()  
    global dfx
    global data
    global tl_df
    global SLP
    global TP
    global EP
    global SIDE
    global riskdf
    
    global SR_QTY
    global OPX_TOKEN
    global TRIGGER
    global LIMIT
    global OPXDF
    global MODE
    
    
    data = pd.read_csv(f'./nifty50_1m.csv')
    data['time']=pd.to_datetime(data['0'])
    dfx=data.set_index(["time"])
    dfx=dfx.between_time('9:15',"15:30")
    dfx.index=pd.to_datetime(dfx.index)
    dfx['atr']=atr_ind(dfx,14)
    dfx=dfx.dropna()
    s="NIFTY50"
    
    q=dfx.iloc[-5]
    u=dfx.iloc[-4]
    o=dfx.iloc[-3]
    p=dfx.iloc[-2]
    a=dfx.iloc[-1]
    
    now = datetime.now().strftime("%H:%M:%S")
    RR=3
    risk=riskdf[-1]
    print('risk= ',risk)
    

    
   
    
    ########################################################  ENTRY LOGIC  #################################################
    
    if  now > starttime   and now < endtime and tl_df[-1] == 0:
        print (f"LOOKING FOR NEW TRADES..at {pivot}")
        print(datetime.now().strftime("%H:%M:%S:%f"),f"------------- atr ={p['atr']}_____________ltp= {dfx.iloc[-1]['close']}")
        print(f'                    ltp=',a['close'],'                                     ')
        print('                                                         ')

                                       ######################    BUY PUT OPX  #########################
            ##BE with 1/2 atr
        if q['high']< pivot and u['high']< pivot and o['open'] < pivot and o['close'] < pivot and o['close'] > o['open'] and  p['close']<o['open'] and o['high'] > pivot and abs(    max(    float(p['open']) - float(p['close']) ,float(o['close'])-float(p['close']))) >= (p['atr']/2): 
            print('                                                         ')
            print('                        _______BE with 1/2 ATR_______                                 ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ', (max(p['high'],o['high'])) ,'Entry= ' , p['close']     )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=PE_token_with_vol(latm,hatm)
            lastval= min(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"p")
            risk=risk*factor
            print('delta = ',1/factor)
               
            
            print(datetime.now().strftime("%H:%M:%S:%f") +" "+  f"buying {token} ")
            
            
            sl= abs(  max(  float(p['high']),float(o['high'])  ) - float(lastval))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)
            
            #------------------------------------
            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')

            f()
             
            RR=float(RR)
            takeprofit=float(lastval-(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=max(p['high'],o['high'])
            stoplossprice=float(stoplossprice)
            cepe= "pe"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
          
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)

            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )


    
    
    
            
        elif q['high']< pivot and u['high']< pivot and o['open'] < pivot and o['close'] < pivot  and   o['high'] > pivot and p['open'] > p['close']  and abs(  max(  float(p['open'])-float(p['close'])  ,float(o['close'])-float(p['close'])  )  ) >= (p['atr']) :
            
            print('                __________bounce > ATR___________                                         ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ', (max(p['high'],o['high'])) ,'Entry= ' , p['close']     )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=PE_token_with_vol(latm,hatm)
            lastval= min(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"p")
            risk=risk*factor
            print('delta = ',1/factor)
               
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(  max(  float(p['high']),float(o['high'])  ) - float(lastval))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)

            #------------------------------------
            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')

            f()
             
            RR=float(RR)
            takeprofit=float(lastval-(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=max(p['high'],o['high'])
            stoplossprice=float(stoplossprice)
            cepe= "pe"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
          
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)

            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
        
        elif q['high']< pivot and u['high']< pivot and o['open'] < pivot and o['close'] < pivot and o['high'] > pivot  and  p['close']< u['open'] and o['close'] > o['open'] and u['close'] > u['open'] and abs(   max (   float(p['open'])-float(p['close']) , float(o['close'])-float(p['close']) )) >= (p['atr']/2) : 
            
            print('                        __________double BE with 1/2 ATR______                                 ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ', (max(p['high'],o['high'])) ,'Entry= ' , p['close']     )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=PE_token_with_vol(latm,hatm)
            lastval= min(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"p")
            risk=risk*factor
            print('delta = ',1/factor)
               
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(  max(  float(p['high']),float(o['high'])  ) - float(lastval))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)

            #------------------------------------
            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')

            f()
             
            RR=float(RR)
            takeprofit=float(lastval-(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=max(p['high'],o['high'])
            stoplossprice=float(stoplossprice)
            cepe= "pe"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
          
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)

            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
            
        elif  q['high']< pivot and u['high']< pivot and  o['high'] < pivot and  p['high'] > pivot and p['close'] < o['open']  and o['open'] < o['close']  :  
           
            print('                     ______BE PINBAR____                                    ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ', (max(p['high'],o['high'])) ,'Entry= ' , p['close']     )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=PE_token_with_vol(latm,hatm)
            lastval= min(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"p")
            risk=risk*factor
            print('delta = ',1/factor)
               
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(  max(  float(p['high']),float(o['high'])  ) - float(lastval))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)

            #------------------------------------
            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')

            f()
             
            RR=float(RR)
            takeprofit=float(lastval-(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=max(p['high'],o['high'])
            stoplossprice=float(stoplossprice)
            cepe= "pe"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
          
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)

            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
            
        elif q['high']< pivot and u['high']< pivot and o['open'] < pivot and o['close'] < pivot  and   o['high'] > pivot and p['open'] > p['close'] and p['close'] < q['open'] and  q['close']> q['open'] and u['close']> u['open']  and abs(  max(  float(p['open'])-float(p['close'])  ,float(o['close'])-float(p['close'])  )  ) >= (p['atr']/2) :
            
            print('                __________bounce = triple BE 1/2 atr__________                                         ')
            print('                                                         ')            
            print(f'pivot level = {pivot}')
            print('                                                         ')
            print('SL= ', (max(p['high'],o['high'])) ,'Entry= ' , p['close']     )
            print('                                                         ')
            latm,hatm=get_atm()
            token,opx,atm=PE_token_with_vol(latm,hatm)
            lastval= min(a['close'],p['close'])
            factor=get_factor(opx,lastval,atm,"p")
            risk=risk*factor
            print('delta = ',1/factor)
            
            print(datetime.now().strftime("%H:%M:%S:%f") +"  "+  f"buying {token} ")
            
            
            sl= abs(  max(  float(p['high']),float(o['high'])  ) - float(lastval))
            qty= lot*(truncate((risk/sl)/lot))
            sr_qty=int(qty)
            
            #------------------------------------
            split=order_slicer(sr_qty,token)

            print(f'ltp=',a['close'],'                                     ')

            f()
             
            RR=float(RR)
            takeprofit=float(lastval-(sl*RR))
            takeprofit=round(takeprofit,2)
            lastval=float(lastval)
            stoplossprice=max(p['high'],o['high'])
            stoplossprice=float(stoplossprice)
            cepe= "pe"

            TP.append(takeprofit)
            EP.append(lastval)
            SLP.append(stoplossprice)
            SIDE.append(cepe)
            #-----------------------------------------------------------------------------
            print ('-----printing notion log-----')
            time.sleep(3)

            RISK=(sl*sr_qty)/factor
            QTY=sr_qty

            DAY=datetime.now().strftime("%A")
            bp=pd.DataFrame(fyers.orderbook()['orderBook'][-split:])
            BUYPRICE=bp['tradedPrice'].mean()
            BUYPRICE=float(BUYPRICE)
            TIME=fyers.orderbook()['orderBook'][-1]['orderDateTime'][12:]
            info = {
                "QTY": {"number": QTY},
                "RISK": {"number":  RISK},
                "BUY PRICE": {"number":  BUYPRICE},

                "DAY": {"rich_text": [{"text": {"content": DAY}}]},
                "TIME": {"rich_text": [{"text": {"content": TIME}}]},
                "SIDE": {"rich_text": [{"text": {"content": cepe}}]},

                "TOKEN": {"title": [{"text": {"content": token}}]},
                "DATE": {"date": {"start": datetime.now().strftime("%Y-%m-%d"), "end": None}}
             }

            create_page(info)
            
            #-------------------------------------------------
          
            SR_QTY.append(sr_qty)
            OPX_TOKEN.append(token)
            DELTA.append(1/factor)


            BUYPRICE=0.05*truncate(BUYPRICE/0.05)
            BUYPRICE=float(BUYPRICE)

            opx_sl=riskdf[-1]/(sr_qty)
            opx_sl=0.05*truncate(opx_sl/0.05)


            opx_slp=float(BUYPRICE-opx_sl)

            LIMIT.append(opx_slp-0.1)
            TRIGGER.append(opx_slp+0.30)

            print("                                                                     ")
            print(f' MAX OPX SL=  {opx_slp} ')
            print(f" 1R opx = {sl*(1/factor)}")
            OPX_1R.append(sl*(1/factor))
            OPXDF=[]
            fyersws.connect()
            MODE.append(1)
            print(f" MODE SWITCHED TO {MODE[-1]}" )
        

            
            #########################################      DONE       ####################################################
            
            
    elif now < starttime and now > "05:10:10":
        print(f"WAITING FOR{starttime} .......")
        print ("NEW DAY NEW MONEY TO BE MADE.....")
        print(datetime.now().strftime("%H:%M:%S")) 
  
        
        
    elif now > endtime:
        print(now)
        print(f"NO NEW TRADES AFTER {endtime}")
        print ("WARS DON'T END WHEN YOU LOSE..... WARS ARE ONLY LOST WHEN ONE GIVES UP")
        
        
        
    else:
        print(datetime.now().strftime("%H:%M:%S"),'trade taken' )

def stop_entry_logic():
    global tl_df
    tl_df.append(1)