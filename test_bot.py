from bot import BasicBot

def test_bot():
    try:
        print("🤖 Initializing Trading Bot...")

        bot = BasicBot()
        print("\n💰 Getting account balance...")
        balance = bot.get_account_balance()
        if balance:
            print("Balance retrieved successfully!")
            for asset in balance:
                if float(asset['balance']) > 0:
                    print(f"  {asset['asset']}: {asset['balance']}")


        print("\n📊 Getting BTC price...")
        btc_price = bot.get_symbol_price("BTCUSDT")
        if btc_price:
            print(f"BTC Price: ${btc_price}")

        print("\n✅ Bot test completed successfully!")

    except Exception as e:
        print(f"❌ Bot test failed: {str(e)}")


if __name__ == '__main__':
    test_bot()