from binance import Client
from binance.exceptions import BinanceAPIException
import config
from logger import setup_logger
import test_connection


class BasicBot:
    def __init__(self , api_key = None , api_secret = None , testnet = True):

        self.api_key = api_key or config.API_Key
        self.api_secret = api_secret or config.API_Secret

        self.testnet = testnet
        self.logger = setup_logger()

        try:
            self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            self.logger.info("Bot initialized successfully")
            self._test_connection()
        except Exception as e:
            self.logger.error(f"Failed to initialize bot: {str(e)}")

    def _test_connection(self):
        try:
            account = self.client.futures_account()
            self.logger.info("API connection successful")
            return True
        except Exception as e:
            self.logger.error(f"API connection failed: {str(e)}")
            return False

    def get_account_balance(self):
        try:
            balance = self.client.futures_account_balance()
            self.logger.info("Retrieved account  balance")
            return balance

        except BinanceAPIException as e:
            self.logger.error(f"Failed to get balance: {str(e)}")
            return None

    def get_symbol_price(self, symbol):
        """get price for symbol"""
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            self.logger.info(f"Price for {symbol}: {price}")
            return price
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get price for {symbol}: {str(e)}")
            return None

    def place_market_order(self , symbol , side , quantity):
        try :
            self.logger.info(f"Placing {side} market order: {quantity} {symbol}")
            if not self._validate_order_inputs(symbol, side, quantity):
                return None

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            self.logger.info(f"Market order placed successfully: {order['orderId']}")
            return order

        except Exception as e:
            self.logger.error(f"Order Failed: {str(e)}")
            return False

    def place_limit_order(self, symbol, side, quantity, price):
        try :
            self.logger.info(f"Placing {side} limit order: {quantity} {symbol} at {price}")

            if not self._validate_order_inputs(symbol, side, quantity, price):
                return None

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',  # Good Till Cancelled
                quantity=quantity,
                price=price
            )

            self.logger.info(f"Limit order placed successfully: {order['orderId']}")
            return order

        except Exception as e:
            self.logger.error(f"place limit Order Failed: {str(e)}")
            return False

    def _validate_order_inputs(self , symbol , side , quantity , price=None):
        if not symbol or len(symbol) < 3:
            self.logger.error("Invalid symbol")
            return False
        if side not in ['BUY' , 'SELL']:
            self.logger.error("Side must be 'BUY' or 'SELL'")
            return False

        try:
            quantity = float(quantity)
            if quantity <= 0:
                self.logger.error("Quantity must be positive")
                return False
        except ValueError:
            self.logger.error("Invalid quantity format")
            return False
        if price is not None:
            try:
                price = float(price)
                if price <= 0:
                    self.logger.error("Price must be positive")
                    return False

            except ValueError:
                self.logger.error("Invalid Price format")
                return False

        return True

    def get_order_status(self , symbol , order_id):
        try:
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            self.logger.info(f"Order {order_id} status: {order['status']}")
            return order
        except BinanceAPIException as e:
            self.logger.error(f"Failed to get order status: {str(e)}")
            return None

"""
for current testing 
"""
bot = BasicBot()

balance = bot.get_account_balance()
