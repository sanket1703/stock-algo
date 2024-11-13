import configparser


def get_test_mode():
    config = configparser.ConfigParser()
    config.read('config.properties')
    return config.getboolean('DEFAULT', 'test_mode')
