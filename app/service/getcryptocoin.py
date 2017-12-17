from coinmarketcap import Market
from domain.tradingexceptions import NoCrytoCurrencyFoundError

RESULT_LIMIT = 1000


class GetCryptoCoin:

    def __init__(self):
        self.api = Market()

    def get_coin(self, symbol):

        for coin in self.api.ticker(limit=RESULT_LIMIT):
            if coin['symbol'] == symbol or coin['name'] == symbol:
                return coin

        if symbol is None:
            raise NoCrytoCurrencyFoundError

    def get_all_coins(self, limit=100):

        coins = []

        for index, coin in enumerate(self.api.ticker()):
            if index < limit:
                coins.append(coin)
            else:
                break

        return coins

    def get_coin_price(self, symbol="btc", numeric=False, amount=1):

        symbol = symbol.upper()
        price = None

        for coin in self.api.ticker(limit=RESULT_LIMIT):
            if coin['symbol'] == symbol or coin['name'] == symbol:
                if numeric:
                    price = float(coin['price_usd']) * float(amount)
                else:
                    price = coin['name']+' : '+coin['symbol']+' : '+'$'+coin['price_usd']+ \
                            ' [1h: '+coin['percent_change_1h']+'%] [24h: '+coin['percent_change_24h']+'%]'
                break

        if price is None:
            print("Didn't find symbol = " + symbol)
            raise NoCrytoCurrencyFoundError

        return price

    def get_coin_amount_by_price(self, symbol="", fiat_amount=""):

        symbol = symbol.upper()
        coin_price = 1

        for coin in self.api.ticker(limit=RESULT_LIMIT):
            if coin['symbol'] == symbol or coin['name'] == symbol:
                coin_price = coin['price_usd']
                break

        amount = float(fiat_amount) / float(coin_price)
        return amount

    def get_top_coins(self, limit=10):

        if int(limit) > 100:
            return "Limit reached. Can only return a maximum of the top 100 coins."

        if int(limit) <= 0:
            return "Top number should be between 1 and 100."

        coin_info = ""

        for coin in self.api.ticker(limit=limit):
            coin_info += "\n "+coin['rank']+". *"+coin['symbol']+"* : *"+coin['name']+"* : *$"+coin['price_usd']+ \
                         '* [1h: ' + coin['percent_change_1h'] + '%] [24h: ' + coin['percent_change_24h'] + '%]'

        return coin_info
