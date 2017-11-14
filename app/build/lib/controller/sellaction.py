import re

from domain.tradetransaction import TradeTransaction
from service.getcryptocoin import GetCryptoCoin
from domain.tradingexceptions import *
from service.getperson import GetPerson
from service.getgameround import GetGameRound
from service.persistsell import PersistSell


class SellAction(TradeTransaction):

    def __init__(self, symbol, coin_amount, player="584142534221"):
        super().__init__(symbol, coin_amount=coin_amount)
        get_crypto_api = GetCryptoCoin()

        self.price = get_crypto_api.get_coin_price(symbol=symbol, numeric=True)
        self.symbol = symbol.upper()
        self.coin_amount = coin_amount
        self.fiat_amount = 0.00
        self.player = GetPerson(number=player).get()
        self.coin = get_crypto_api.get_coin(symbol=self.symbol)

    def persist(self):
        """
        Check if player is part fo current round
        """
        get_game_round = GetGameRound()
        current_game = get_game_round.get_current()

        if not get_game_round.is_player_in_round(current_game, self.player):
            raise PlayerIsNotPartOfGameRoundError

        PersistSell().persist(self)

        worth_amount = "%.2f" % float(self.fiat_amount)
        amount_formatted = "%.8f" % float(self.coin_amount)

        return self.player.name+", you sold " + amount_formatted + " of " + self.coin['name'] + " worth $"+worth_amount
