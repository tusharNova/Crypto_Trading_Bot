import sys
from bot import BasicBot
from logger import setup_logger

class TradingCLI:
    def __init__(self):
        self.bot = BasicBot()
        self.logger = setup_logger()

    def display_menu(self):
        print("\n" + "=" * 50)
        print("🚀 CRYPTO TRADING BOT - TESTNET")
        print("=" * 50)
        print("1. 💰 View Account Balance")
        print("2. 📊 Get Symbol Price")
        print("3. 🛒 Place Market Order (Buy/Sell)")
        print("4. 📈 Place Limit Order (Buy/Sell)")
        print("5. 🛡️  Place Stop-Limit Order (Advanced)")
        print("6. 🔍 Check Order Status")
        print("7. ❌ Exit")
        print("=" * 50)

    def get_user_input(self , prompt , input_type = str , validation = None):

        while True:
            try :
                user_input = input(prompt)
                if user_input.lower()in ['quit' ,'exit' , 'q']:
                    print("Good Bye .. .! ")
                    sys.exit(0)

                converted_input = input_type(user_input)

                if validation and not validation(converted_input):
                    print("❌ Invalid input. Please try again.")
                    continue
                return converted_input

            except ValueError:
                print(f"❌ Please enter a valid {input_type.__name__}")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                sys.exit(0)

    def view_balance(self):
        print("\n📊 Getting Account Balance...")
        balance = self.bot.get_account_balance()
        if balance:
            print("\n💰 Current Balance:")
            print("-" * 30)
            for asset in balance:
                if float(asset['balance']) > 0:
                    print(f"  {asset['asset']}: {asset['balance']}")
        else:
            print("❌ Failed to retrieve balance")

    def get_symbol_price(self):
        """Get and display symbol price"""
        print("\n📊 Get Symbol Price")
        print("Popular symbols: BTCUSDT, ETHUSDT, ADAUSDT, DOTUSDT")
        symbol = self.get_user_input(
            "Enter symbol (e.g., BTCUSDT): ",
            str,
            lambda x: len(x) >= 6 and x.upper().endswith('USDT')
        ).upper()
        price = self.bot.get_symbol_price(symbol)
        if price:
            print(f"💵 Current price of {symbol}: ${price:,.2f}")
        else:
            print("❌ Failed to get price. Check if symbol is valid.")

    def place_market_order(self):
        """Place a market order"""
        print("\n🛒 Place Market Order")
        print("⚠️  Market orders execute immediately at current market price")
        symbol = self.get_user_input(
            "Enter symbol (e.g., BTCUSDT): ",
            str,
            lambda x: len(x) >= 6
        ).upper()

        current_price = self.bot.get_symbol_price(symbol)
        if current_price:
            print(f"📊 Current {symbol} price: ${current_price:,.2f}")

        side = self.get_user_input(
            "Enter order side (BUY/SELL): ",
            str,
            lambda x: x.upper() in ['BUY', 'SELL']
        ).upper()

        quantity = self.get_user_input(
            "Enter quantity: ",
            float,
            lambda x: x > 0
        )
        print(f"\n📝 Order Summary:")
        print(f"   Symbol: {symbol}")
        print(f"   Side: {side}")
        print(f"   Type: MARKET")
        print(f"   Quantity: {quantity}")
        print(f"   Estimated cost: ~${current_price * quantity:,.2f}" if current_price else "")

        confirm = self.get_user_input(
            "\n⚠️  Confirm order? (yes/no): ",
            str,
            lambda x: x.lower() in ['yes', 'no', 'y', 'n']
        ).lower()

        if confirm in ['yes', 'y']:
            print("🚀 Placing market order...")
            order = self.bot.place_market_order(symbol, side, quantity)

            if order:
                print("✅ Order placed successfully!")
                print(f"   Order ID: {order['orderId']}")
                print(f"   Status: {order['status']}")
                print(f"   Executed Quantity: {order.get('executedQty', 'N/A')}")
            else:
                print("❌ Failed to place order. Check logs for details.")
        else:
            print("❌ Order cancelled")

    def place_limit_order(self):
        """Place a limit order"""
        print("\n📈 Place Limit Order")
        print("ℹ️  Limit orders execute only at your specified price or better")
        
        symbol = self.get_user_input(
            "Enter symbol (e.g., BTCUSDT): ",
            str,
            lambda x: len(x) >= 6
        ).upper()

        current_price = self.bot.get_symbol_price(symbol)
        if current_price:
            print(f"📊 Current {symbol} price: ${current_price:,.2f}")
        side = self.get_user_input(
            "Enter order side (BUY/SELL): ",
            str,
            lambda x: x.upper() in ['BUY', 'SELL']
        ).upper()

        quantity = self.get_user_input(
            "Enter quantity: ",
            float,
            lambda x: x > 0
        )
        price = self.get_user_input(
            "Enter limit price: $",
            float,
            lambda x: x > 0
        )

        if current_price:
            difference = ((price - current_price) / current_price) * 100
            print(f"📊 Your price vs current: {difference:+.2f}%")

            # Confirmation
        print(f"\n📝 Order Summary:")
        print(f"   Symbol: {symbol}")
        print(f"   Side: {side}")
        print(f"   Type: LIMIT")
        print(f"   Quantity: {quantity}")
        print(f"   Price: ${price}")
        print(f"   Total: ${price * quantity:,.2f}")

        confirm = self.get_user_input(
            "\n⚠️  Confirm order? (yes/no): ",
            str,
            lambda x: x.lower() in ['yes', 'no', 'y', 'n']
        ).lower()

        if confirm in ['yes', 'y']:
            print("🚀 Placing limit order...")
            order = self.bot.place_limit_order(symbol, side, quantity, price)

            if order:
                print("✅ Order placed successfully!")
                print(f"   Order ID: {order['orderId']}")
                print(f"   Status: {order['status']}")
                print("ℹ️  Limit order will execute when price reaches your target")
            else:
                print("❌ Failed to place order. Check logs for details.")
        else:
            print("❌ Order cancelled")

        current_price = self.bot.get_symbol_price(symbol)
        if current_price:
            print(f"📊 Current {symbol} price: ${current_price:,.2f}")

        side = self.get_user_input(
            "Enter order side (BUY/SELL): ",
            str,
            lambda x: x.upper() in ['BUY', 'SELL']
        ).upper()


    def check_order_status(self):
        """Check order status"""
        print("\n🔍 Check Order Status")
        symbol = self.get_user_input(
            "Enter symbol: ",
            str,
            lambda x: len(x) >= 6
        ).upper()
        order_id = self.get_user_input(
            "Enter order ID: ",
            int,
            lambda x: x > 0
        )
        print("🔍 Checking order status...")
        order = self.bot.get_order_status(symbol, order_id)
        if order:
            print("📋 Order Details:")
            print(f"   Order ID: {order['orderId']}")
            print(f"   Symbol: {order['symbol']}")
            print(f"   Status: {order['status']}")
            print(f"   Side: {order['side']}")
            print(f"   Type: {order['type']}")
            print(f"   Quantity: {order['origQty']}")
            print(f"   Executed: {order['executedQty']}")
            if 'price' in order:
                print(f"   Price: ${order['price']}")
        else:
            print("❌ Failed to get order status")

    def place_stop_limit_order(self):
        """Place a stop-limit order"""
        print("\n🛡️  Place Stop-Limit Order")
        print("ℹ️  Stop-limit combines stop-loss protection with price control")
        print("   • Stop Price: Triggers the order when market reaches this level")
        print("   • Limit Price: Maximum/minimum price you're willing to pay/receive")

        # Get order details
        symbol = self.get_user_input(
            "Enter symbol (e.g., BTCUSDT): ",
            str,
            lambda x: len(x) >= 6
        ).upper()

        # Get current price for reference
        current_price = self.bot.get_symbol_price(symbol)
        if current_price:
            print(f"📊 Current {symbol} price: ${current_price:,.2f}")

        side = self.get_user_input(
            "Enter order side (BUY/SELL): ",
            str,
            lambda x: x.upper() in ['BUY', 'SELL']
        ).upper()

        quantity = self.get_user_input(
            "Enter quantity: ",
            float,
            lambda x: x > 0
        )

        # Explain stop-limit logic based on side
        if side == 'BUY':
            print("💡 For BUY orders:")
            print("   Stop Price: Should be ABOVE current price")
            print("   Limit Price: Maximum you'll pay (usually above stop price)")
        else:
            print("💡 For SELL orders:")
            print("   Stop Price: Should be BELOW current price")
            print("   Limit Price: Minimum you'll accept (usually below stop price)")

        stop_price = self.get_user_input(
            "Enter stop price: $",
            float,
            lambda x: x > 0
        )

        limit_price = self.get_user_input(
            "Enter limit price: $",
            float,
            lambda x: x > 0
        )

        # Show analysis
        if current_price:
            stop_diff = ((stop_price - current_price) / current_price) * 100
            limit_diff = ((limit_price - current_price) / current_price) * 100
            print(f"📊 Stop vs current: {stop_diff:+.2f}%")
            print(f"📊 Limit vs current: {limit_diff:+.2f}%")

        # Confirmation
        print(f"\n📝 Stop-Limit Order Summary:")
        print(f"   Symbol: {symbol}")
        print(f"   Side: {side}")
        print(f"   Type: STOP-LIMIT")
        print(f"   Quantity: {quantity}")
        print(f"   Stop Price: ${stop_price}")
        print(f"   Limit Price: ${limit_price}")
        print(f"   Max Cost: ${limit_price * quantity:,.2f}")

        confirm = self.get_user_input(
            "\n⚠️  Confirm stop-limit order? (yes/no): ",
            str,
            lambda x: x.lower() in ['yes', 'no', 'y', 'n']
        ).lower()

        if confirm in ['yes', 'y']:
            print("🚀 Placing stop-limit order...")
            order = self.bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)

            if order:
                print("✅ Stop-limit order placed successfully!")
                print(f"   Order ID: {order['orderId']}")
                print(f"   Status: {order['status']}")
                print("ℹ️  Order will activate when market hits stop price")
            else:
                print("❌ Failed to place order. Check logs for details.")
        else:
            print("❌ Order cancelled")

    def run(self):
        """Main CLI loop"""
        print("🚀 Welcome to Crypto Trading Bot!")
        print("💡 Type 'quit' or 'exit' anytime to close the program")

        while True:
            try:
                self.display_menu()
                choice = self.get_user_input(
                    "Select an option (1-7): ",
                    str,
                    lambda x: x in ['1', '2', '3', '4', '5', '6', '7']
                )
                if choice == '1':
                    self.view_balance()
                elif choice == '2':
                    self.get_symbol_price()
                elif choice == '3':
                    self.place_market_order()
                elif choice == '4':
                    self.place_limit_order()
                elif choice == '5':
                    self.check_order_status()
                elif choice == '6':
                    self.check_order_status()

                elif choice == '7':
                    print("👋 Thanks for using Trading Bot!")
                    break

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                print(f"❌ An error occurred: {str(e)}")


if __name__ == '__main__':
    cli = TradingCLI()
    cli.run()

