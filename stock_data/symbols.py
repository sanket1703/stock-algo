import json


def remove_suffix(symbol, suffix=".NS"):
    return symbol.replace(suffix, "")


def get_symbol_token(nse_stock_code):
    symbol_token_name = remove_suffix(nse_stock_code)
    file_path="stock_data/data/stock_token.json"
    with open(file_path, "r") as json_file:
        stock_data = json.load(json_file)
    return stock_data.get(symbol_token_name)


if __name__ == "__main__":
    print(get_symbol_token("RELIANCE.f"))


