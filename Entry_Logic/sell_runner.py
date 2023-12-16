from utils.data import get_s_data 
from trade_exec import SELL_EXE

def start_sell_runner():

# SELL LEVEL PIVOT
    selllev=[
        
        21004.45,
        21005.75

    ]

    tl_df=[0]
    while tl_df[-1]==0:
        time.sleep(.2)
        
        get_s_data()
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('                                                  ')
        for pivot in selllev: 
            SELL_EXE(pivot,lot)

            
    TAR.append(0.0)
    LIQ=[100000.0]
    PB=[0]  
    print("TAR=",TAR[-1])