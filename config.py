import os
from dotenv import load_dotenv
import os
load_dotenv()

API_Key =os.getenv('API_Key')
API_Secret = os.getenv('API_Secret')

TESTNET = True
BASE_URL = 'https://testnet.binancefuture.com/'

DEFAULT_SYMBOL = "BTCUSDT"
MIN_ORDER_SIZE = 0.001