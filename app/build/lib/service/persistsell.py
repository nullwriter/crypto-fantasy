from domain.tabledef import CryptoStock, BoughtCryptoStock, PortfolioStock
from service.getportfolio import GetPortfolio
from domain.tradingexceptions import CryptoCurrencyNotFoundInPortfolio, NotEnoughCryptoCoinError
from service.contextmanager import session_scope
from service.getcryptocoin import GetCryptoCoin


class PersistSell:

    def __init__(self):
        pass

    def persist(self, action):

        portfolio = GetPortfolio(action.player).get()

        with session_scope() as session:
            crypto_stock = session.query(CryptoStock).filter_by(symbol=action.symbol).first()
            portfolio_stock = session.query(PortfolioStock).filter_by(
                crypto_stock_id=crypto_stock.id,
                portfolio_id=portfolio.id
            ).first()

        if portfolio_stock is None:
            raise CryptoCurrencyNotFoundInPortfolio

        if '$' in action.coin_amount:
            """
            Sell is made by choosing usd equivalent, need to find coin equivalent
            """
            fiat_amount = action.clean_arg(action.coin_amount)
            action.coin_amount = GetCryptoCoin().get_coin_amount_by_price(symbol=crypto_stock.symbol, fiat_amount=fiat_amount)
            action.fiat_amount = fiat_amount
        else:
            action.fiat_amount = self.get_fiat_amount(action.coin_amount, action.price)

        coin_left = float(portfolio_stock.coin_amount) - float(action.coin_amount)

        if coin_left < 0:
            raise NotEnoughCryptoCoinError

        new_fiat_amount = float(portfolio.fiat_amount) + float(action.fiat_amount)

        if coin_left > 0:

            portfolio_stock.coin_amount = coin_left
            with session_scope() as session:
                session.add(portfolio_stock)

        elif coin_left == 0:
            """
            If no coin left, remove from bought coins and from portfolio stocks
            """
            with session_scope() as session:
                session.delete(portfolio_stock)
                bought_crypto = session.query(BoughtCryptoStock).filter_by(crypto_stock_id=crypto_stock.id).all()

            for crypto in bought_crypto:
                with session_scope() as session:
                    session.delete(crypto)

        portfolio.fiat_amount = new_fiat_amount
        with session_scope() as session:
            session.add(portfolio)

    def get_fiat_amount(self, coin_amount, price):
        return float(coin_amount) * float(price)
