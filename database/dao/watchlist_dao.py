import configparser

# Initialize the configparser
config = configparser.ConfigParser()

# Read the config file
config.read('config.properties')
env = config['DEFAULT']['environment']

def get_watchlist(db):
    watchlist = db.Table('watchlist'+ env)
    curent_watchlist = watchlist.scan()['Items'][0]['watchlist']
    return curent_watchlist
    

def update_watchlist(db,update_watchlist):

    watchlist = db.Table('watchlist'+ env)
    key = {"watchlist_id":"1"}
    response = watchlist.get_item(Key=key)
    print(response)
    response['Item']['watchlist'] = update_watchlist
    watchlist.put_item(Item = response['Item'])
    return update_watchlist