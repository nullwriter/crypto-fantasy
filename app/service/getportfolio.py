from domain.tabledef import Portfolio, BoughtCryptoStock, CryptoStock, PortfolioStock
from service.getgameround import GetGameRound
from domain.tradingexceptions import NoStocksInPortfolioError, PlayerIsNotPartOfGameRoundError, \
    NoCrytoCurrencyFoundError
from service.getcryptocoin import GetCryptoCoin
from service.contextmanager import session_scope
import math


class GetPortfolio:

    def __init__(self, person=""):
        self.person = person
        self.get_game_round = GetGameRound()

    def get(self):

        game_round = self.get_game_round.get_current()
        game_round_player = self.get_game_round.get_game_round_player(game_round, self.person)

        with session_scope() as session:
            portfolio = session.query(Portfolio).filter_by(
                game_round_player_id=game_round_player.id).first()

        if portfolio is None:
            raise PlayerIsNotPartOfGameRoundError

        return portfolio

    def get_by_game_round_player(self, game_round_player):

        with session_scope() as session:
            portfolio = session.query(Portfolio).filter_by(
                game_round_player_id=game_round_player.id).first()

        if portfolio is None:
            raise PlayerIsNotPartOfGameRoundError

        return portfolio

    def get_crypto_value(self, portfolio):

        with session_scope() as session:
            stocks = session.query(PortfolioStock).filter_by(portfolio_id=portfolio.id).all()

        if stocks is None:
            raise NoStocksInPortfolioError

        get_coin = GetCryptoCoin()
        current_crypto_value = 0

        for stock in stocks:

            with session_scope() as session:
                crypto = session.query(CryptoStock).filter_by(id=stock.crypto_stock_id).first()

            current_price = get_coin.get_coin_price(
                symbol=crypto.symbol,
                numeric=True,
                amount=stock.coin_amount
            )

            current_crypto_value += current_price

        return current_crypto_value

    def print(self, portfolio):

        with session_scope() as session:
            stocks = session.query(PortfolioStock).filter_by(portfolio_id=portfolio.id).all()

        if stocks is None:
            raise NoStocksInPortfolioError

        portfolio_string = self.person.name+"'s Portfolio\n--------------------\n"
        current_crypto_value = 0

        for stock in stocks:

            with session_scope() as session:
                crypto = session.query(CryptoStock).filter_by(id=stock.crypto_stock_id).first()

            try:
                current_price = GetCryptoCoin().get_coin_price(
                    symbol=crypto.symbol,
                    numeric=True,
                    amount=stock.coin_amount
                )
            except NoCrytoCurrencyFoundError:
                current_price = 0

            current_value = "$%.2f" % current_price
            initial_value = float(stock.buy_price) * float(stock.coin_amount)

            nice_string = crypto.symbol + " " + str(stock.coin_amount)+" - "+current_value

            value_change = self.get_price_change(current_price, initial_value)
            if initial_value != 0:
                """
                This check is added since this functionality is new and the data is not in all players at the moment.
                """
                nice_string += " ("+value_change+")"

            current_crypto_value += current_price
            portfolio_string += nice_string+"\n"

        total_value = current_crypto_value + float(portfolio.fiat_amount)

        portfolio_string += "--------------------\n"\
                            "USD: $"+str(portfolio.fiat_amount)+"\n" \
                            "Crypto value: $"+str("%.2f" % current_crypto_value)+"\n" \
                            "Total value: $"+str("%.2f" % total_value)+"\n"

        return portfolio_string

    @staticmethod
    def get_price_change(current_price, initial_value):

        indicator = "+"
        value_change = abs(float(current_price) - float(initial_value))

        if current_price < initial_value:
            indicator = "-"

        return indicator + "$%.2f" % value_change
