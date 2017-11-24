from controller import BOT_ORM_SESSION
from service.contextmanager import session_scope
from domain.tabledef import CryptoStock, BoughtCryptoStock, PortfolioStock
from service.getportfolio import GetPortfolio
from domain.tradingexceptions import NotEnoughMoneyError


class PersistBuy:

    def __init__(self):
        self.session = BOT_ORM_SESSION()

    def persist(self, action):

        with session_scope() as session:
            crypto_stock = session.query(CryptoStock).filter_by(symbol=action.symbol).first()

        portfolio = GetPortfolio(action.player).get()
        fiat_left = float(portfolio.fiat_amount) - float(action.fiat_amount)

        if fiat_left < 0:
            raise NotEnoughMoneyError

        """
        If Crypto doesn't exist, lets add it to our collection while we're at it
        """
        if crypto_stock is None:
            print("Crypto stock asked to buy does not exist")
            crypto_stock = CryptoStock(
                name=action.coin['name'],
                symbol=action.coin['symbol'],
                slug=action.coin['id']
            )

            with session_scope() as session:
                session.add(crypto_stock)

        bought_crypto = BoughtCryptoStock(
            crypto_stock_id=crypto_stock.id,
            at_price=action.price,
            coin_amount=action.coin_amount,
            fiat_amount=action.fiat_amount,
            portfolio_id=portfolio.id
        )

        """
        Lets add to accumulated PortfolioStock table
        """
        with session_scope() as session:
            portfolio_stock = session.query(PortfolioStock).filter_by(
                crypto_stock_id=crypto_stock.id,
                portfolio_id=portfolio.id
            ).first()

        if portfolio_stock is None:
            """Lets add it"""
            portfolio_stock = PortfolioStock(
                portfolio_id=portfolio.id,
                crypto_stock_id=crypto_stock.id,
                coin_amount=action.coin_amount,
                buy_price=action.price
            )
        else:
            """Lets increment amount"""
            current_amount = portfolio_stock.coin_amount
            portfolio_stock.coin_amount = float(current_amount) + action.coin_amount

        portfolio.fiat_amount = fiat_left

        with session_scope() as session:
            session.add(portfolio_stock)
            session.add(portfolio)
            session.add(bought_crypto)

        return True
