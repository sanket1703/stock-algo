from utils.database_helper.client import clear_trade_log_clients
from utils.database_helper.slots import clean_slots

def clear_stack():
    clients = ["FTCT1208","KEYUR","SANKET","Smit","Sid"]
    clear_trade_log_clients(clients)
    clean_slots()

if __name__ == "__main__":
    clear_stack()