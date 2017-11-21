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

        with session_scope() as session:
            session.add(bought_crypto)

        """
        Lets calculate new buy price based on current & previous buys
        """
        with session_scope() as session:
            previous_bought_crypto = session.query(BoughtCryptoStock).filter_by(
                crypto_stock_id=crypto_stock.id,
                portfolio_id=portfolio.id
            ).all()

        coin_amount = float(action.coin_amount)
        fiat_amount = float(action.fiat_amount)
        new_buy_price = float(action.price)

        if previous_bought_crypto:
            for pbc in previous_bought_crypto:
                coin_amount += float(pbc.coin_amount)
                fiat_amount += float(pbc.fiat_amount)

            new_buy_price = float(fiat_amount) / float(coin_amount)

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
                coin_amount=coin_amount,
                buy_price=new_buy_price
            )
        else:
            """Lets increment amount"""
            portfolio_stock.coin_amount = coin_amount
            portfolio_stock.buy_price = new_buy_price

        portfolio.fiat_amount = fiat_left

        with session_scope() as session:
            session.add(portfolio_stock)
            session.add(portfolio)

        return True
