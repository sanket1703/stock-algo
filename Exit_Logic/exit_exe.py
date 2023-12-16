def exit_execute():
    global SLP
    global riskdf
    global SIDE
    global tl_df
    global SR_QTY
    global OPX_TOKEN
    global OPX_BUYPRICE
    global TRIGGER
    global LIMIT
    global MODE
    global NIFTYDF
    global OPXDF
    global counter
    global lot
    
    global PB
    global LIQ
    global PBLEV
    global TAR
    
    counter+=1
    
    
    
    if OPXDF[-1] <= TRIGGER[-1]:

        SL_slicer(SR_QTY[-1],OPX_TOKEN[-1],LIMIT[-1])

        MODE.append(0)
        f()
        print("                                         ")
        print(OPXDF[-1]," <= " ,TRIGGER[-1])
        print("                                         ")

        print(" __OPX MAX SL__ "* 50)
        time.sleep(2)


    elif OPXDF[-1] >= (LIQ[-1]-1.7):
        
        SL_slicer(SR_QTY[-1],OPX_TOKEN[-1],LIQ[-1])

        MODE.append(0)
        f()
        print("                                         ")
        print(OPXDF[-1]," >= " ,LIQ[-1])
        print("                                         ")
        

    elif SIDE[-1]=="ce":
        
        if NIFTYDF[-1] <= SLP[-1]:
            
            SL_slicer(SR_QTY[-1],OPX_TOKEN[-1],LIMIT[-1])
                
            MODE.append(0)
            f()
            print("                                         ")
            print(NIFTYDF[-1]," <= " ,SLP[-1])
            print("                                         ")
           
            print(" __nifty sl__ "* 50)
            time.sleep(2)
        
        elif NIFTYDF[-1] >= TAR[-1]:
            
            SL_slicer_MARKET(SR_QTY[-1],OPX_TOKEN[-1])
                
            MODE.append(0)
            f()
            print("                                         ")
            print(NIFTYDF[-1]," >= " ,TAR[-1])
            print("                                         ")
           
            print(" __nifty TAR__ "* 50)
            time.sleep(2)
            
        elif PB[-1] == 1:
            
            if NIFTYDF[-1] >= PBLEV[-1]:
                
                PB.append(0) 
                q=(SR_QTY[-1]/2)
                q=lot*math.ceil(q/lot)
                q=int(q)
                SR_QTY.append(SR_QTY[-1]-q)
                
                SL_slicer_MARKET(q,OPX_TOKEN[-1])
                
                print("partial booked _"*5)
                print("                                               ")
                print("                                               ")
                print("                                               ")
                print(f"Total REMAINING QTY = {SR_QTY[-1]}  ")
                print("                                               ")
                print("                                               ")
                print("                                               ")
        
        elif counter >=100:
            counter=0
            print(datetime.now().strftime("%H:%M:%S:%f") )
            print("                                         ")
            print("                                         ")
            print(f"Total QTY = {SR_QTY[-1]}  ")
            print(f"long {OPX_TOKEN[-1]}")
            print("                                         ")
            print("nifty ltp = ",NIFTYDF[-1])
            print("nifty SL = ",SLP[-1])
            print("                                         ")
            print("                                         ")
            print("OPX ltp = ",OPXDF[-1])
            print("TRIGGER = ",TRIGGER[-1])
            print("opx sl = ",LIMIT[-1]+0.1)
            print("                                         ")
            print("PB = ",PB[-1])
            print("PBLEV = ",PBLEV[-1])
            print("                                         ")
            print("TAR = ",TAR[-1])
            print("LIQ = ",LIQ[-1])
            
            print("_________________________________                 ")




    elif SIDE[-1]=="pe":
        
        if NIFTYDF[-1] >= SLP[-1]:

            SL_slicer(SR_QTY[-1],OPX_TOKEN[-1],LIMIT[-1])
                
            MODE.append(0)
            f()
            print("                                         ")
            print(NIFTYDF[-1]," >= " ,SLP[-1])
            print("                                         ")
            
            print(" __nifty sl__ "* 50)
            time.sleep(2)
            
        elif NIFTYDF[-1] <= TAR[-1]:
            
            SL_slicer_MARKET(SR_QTY[-1],OPX_TOKEN[-1])
                
            MODE.append(0)
            f()
            print("                                         ")
            print(NIFTYDF[-1]," <= " ,TAR[-1])
            print("                                         ")
           
            print(" __nifty TAR__ "* 50)
            time.sleep(2)
            
        elif PB[-1] == 1:
            
            if NIFTYDF[-1] <= PBLEV[-1]:
                
                PB.append(0) 
                q=(SR_QTY[-1]/2)
                q=lot*math.ceil(q/lot)
                q=int(q)
                SR_QTY.append(SR_QTY[-1]-q)
                
                SL_slicer_MARKET(q,OPX_TOKEN[-1])
                
                print("partial booked _"*5)
                print("                                               ")
                print("                                               ")
                print("                                               ")
                print(f"Total REMAINING QTY = {SR_QTY[-1]}  ")
                print("                                               ")
                print("                                               ")
                print("                                               ")
        
        
        elif counter >=100:
            counter=0
            print(datetime.now().strftime("%H:%M:%S:%f") )
            print("                                         ")
            print("                                         ")
            print(f"Total QTY = {SR_QTY[-1]}  ")
            print(f"long {OPX_TOKEN[-1]}")
            print("                                         ")
            print("nifty ltp = ",NIFTYDF[-1])
            print("nifty SL = ",SLP[-1])
            print("                                         ")
            print("                                         ")
            print("OPX ltp = ",OPXDF[-1])
            print("TRIGGER = ",TRIGGER[-1])
            print("opx sl = ",LIMIT[-1]+0.1)
            print("                                         ")
            print("PB = ",PB[-1])
            print("PBLEV = ",PBLEV[-1])
            print("                                         ")
            print("TAR = ",TAR[-1])
            print("LIQ = ",LIQ[-1])
            
            print("_________________________________                 ")