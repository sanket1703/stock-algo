## BUY CALL LEVEL PIVOT##

from utils.data import get_s_data 
from DTS.Entry_Logic.trade_exec import BUY_EXE
from DTS.Exit_Logic.exit_exe import EXIT_EXE
from Verification import verification
import time

def start_buy_runner(buylev):
    
    # TODO:- Make it a parameter
    buylev=[ 20953.70,20950.60]
    lot = 50
    
    # TODO:- This is a global Variable
    tl_df=[0]
    
    while tl_df[-1]==0:
        time.sleep(.2)
        
        get_s_data()
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('                                                  ')
        for pivot in buylev:
            BUY_EXE(pivot,lot)

            
    # TODO:- Handle the DataFrame Septy        
    TAR.append(100000.0)
    LIQ=[100000.0]
    PB=[0]  
    print("TAR=",TAR[-1])
    
    # Initiate the Verification Process before action
    
        