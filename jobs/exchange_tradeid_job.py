import json
import csv
from datetime import datetime
from utils.json.helper import get_filled_buy_orders, get_filled_sell_orders
from loguru import logger
from notification.email.send_email import send_email

def exchange_tradeid_job():
    logger.info("Extraction of Exchange Trade Id started.")
    buy_trade_ids = extract_trade_ids(get_filled_buy_orders())
    sell_trade_id = extract_trade_ids(get_filled_sell_orders())
    trade_ids = buy_trade_ids + sell_trade_id
    # Get today's date to create the filename
    today_date = datetime.today().strftime('%Y-%m-%d')
    filename = f"order_book/trades/{today_date}_TRADEID.csv"
    # Save trade IDs into a CSV file with SNO
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SNO", "Exchg Order ID"])  # Header for the CSV file
        for index, trade_id in enumerate(trade_ids, start=1):
            writer.writerow([index, trade_id])

    logger.info(f"Trade IDs with SNO have been saved in {filename}.")
    sender = "Keyursanket.com"
    recipient = "sanketyou8@gmail.com"
    cc="keyurmarolia2@gmail.com"
    subject = f"Exchange trade IDs for {today_date}"
    body = f"Please find attached the exchange trade ids on {today_date} saved in {today_date}_TRADEID.csv"
    logger.info("Sending email of the csv.")
    send_email(sender,recipient,cc,subject,body,filename)
    logger.info("Extraction of Exchange Trade Id completed.")


def extract_trade_ids(data):
    trade_ids = []
    for user, trades in data.items():
        for trade in trades:
            if user=="date":
                continue
            trade_id = trade[2]  # The trade ID is the third element in each list
            trade_ids.append(trade_id)

    return trade_ids


