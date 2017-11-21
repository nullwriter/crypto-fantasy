import re

from domain.tradetransaction import TradeTransaction
from service.getcryptocoin import GetCryptoCoin
from service.persistbuy import PersistBuy
from domain.tradingexceptions import PlayerIsNotPartOfGameRoundError
from service.getperson import GetPerson
from service.getgameround import GetGameRound


class BuyAction(TradeTransaction):

    def __init__(self, symbol, fiat_amount, player=""):
        super().__init__(symbol, fiat_amount=fiat_amount)
        get_crypto_api = GetCryptoCoin()

        self.price = get_crypto_api.get_coin_price(symbol=symbol, numeric=True)
        self.symbol = self.clean_arg(symbol.upper())
        self.player = GetPerson(number=player).get()
        self.coin_amount = self.get_coin_amount()
        self.coin = get_crypto_api.get_coin(symbol=self.symbol)

    def persist(self):
        """
        Check if player is part of current round
        """
        get_game_round = GetGameRound()
        current_game = get_game_round.get_current()

        if not get_game_round.is_player_in_round(current_game, self.player):
            raise PlayerIsNotPartOfGameRoundError

        PersistBuy().persist(self)
        amount_formatted = "%.8f" % self.coin_amount
        return self.player.name+", you bought " + amount_formatted + " of " + self.coin['name']

    def get_coin_amount(self):
        return float(self.fiat_amount) / float(self.price)
