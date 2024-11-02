import json
from loguru import logger

def empty_json(file_path):
    # Read the JSON data from the file
    with open(file_path, 'r') as file:
        orders = json.load(file)

    # Update client codes to empty lists, ignoring the 'date' field
    for client in orders:
        if client != "date":
            orders[client] = []

    # Write the updated JSON back to the file
    with open(file_path, 'w') as file:
        json.dump(orders, file, indent=4)

    logger.info(f"Order JSON at {file_path} has been reset successfully.")


def clean_order_jsons_job():
    file_paths = [
        "order_book/buy_orders.json",
        "order_book/sell_orders.json",
        "order_book/filled_orders/filled_buy_orders.json",
        "order_book/filled_orders/filled_sell_orders.json",
        "order_book/unfilled_orders/unfilled_buy_orders.json",
        "order_book/unfilled_orders/unfilled_sell_orders.json"
    ]
    for file_path in file_paths:
        empty_json(file_path)