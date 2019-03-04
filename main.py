import requests
import time
from pprint import pprint
from stock_bot import StockBot

api_token = "SUP3R S3CR3T K3Y"
bot = StockBot(api_token)

while True:

    print("Update...")
    print("-" * 20)

    bot.serve_updates()

    