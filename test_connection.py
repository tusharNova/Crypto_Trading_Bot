from binance.client import Client
import sys
from dotenv import load_dotenv
import os
load_dotenv()

import time
API_Key =os.getenv('API_Key')
API_Secret = os.getenv('API_Secret')


def test_connection():
    try:

        client = Client(API_Key , API_Secret , testnet=True)
        # Test basic connection
        print("Testing connection...")

        # Get account info
        account = client.futures_account()
        print("✅ Connection successful!")
        print(f"Account type: {account.get('feeTier', 'N/A')}")
        # Get current balance
        balance = client.futures_account_balance()
        print("\n📊 Account Balances:")
        for asset in balance:
            if float(asset['balance']) > 0:
                print(f"  {asset['asset']}: {asset['balance']}")

        # Test getting symbol info
        exchange_info = client.futures_exchange_info()
        print(f"\n📈 Available symbols: {len(exchange_info['symbols'])} pairs")

        return True

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False


if __name__ == '__main__':
    test_connection()

# if __name__ == '__main__':
#