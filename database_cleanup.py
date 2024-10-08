from utils.database_helper.client import clear_trade_log_clients
from utils.database_helper.slots import clean_slots

def clear_stack():
    # clients = ["SIM1208","SIM1211"]
    # clear_trade_log_clients(clients)
    clean_slots()

if __name__ == "__main__":
    clear_stack()