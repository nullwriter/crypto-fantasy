import re


class TradeTransaction(object):

    def __init__(self, symbol, coin_amount="", fiat_amount=""):
        self.symbol = symbol
        self.coin_amount = coin_amount
        self.fiat_amount = self.clean_arg(fiat_amount)

    @staticmethod
    def clean_arg(arg):
        return re.sub('[^A-Za-z0-9]+', '', arg)
