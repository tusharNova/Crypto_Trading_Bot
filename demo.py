from  binance.client import Client
from dotenv import load_dotenv
import pandas as pd
import os
load_dotenv()

import time
API_Key =os.getenv('API_Key')
API_Secret = os.getenv('API_Secret')


# print(API_Secret , API_Secret)
client = Client(API_Key , API_Secret , testnet=True)
tickers = client.get_all_tickers()

print(client.futures_account())