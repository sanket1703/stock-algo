import configparser

# Initialize the configparser
config = configparser.ConfigParser()

# Read the config file
config.read('config.properties')
env = config['DEFAULT']['environment']

def get_slots(db):
    slots = db.Table('stock_slots'+ env)
    current_slots = slots.scan()['Items'][0]['stock_slots']
    return current_slots
    

def update_slots(db,update_slots):
    
    slots = db.Table('stock_slots'+ env)
    key = {"stock_slots_id":"1"}
    response = slots.get_item(Key=key)
    print(response)
    response['Item']['stock_slots'] = update_slots
    slots.put_item(Item = response['Item'])
    print(response['Item']['stock_slots'])
    return update_slots