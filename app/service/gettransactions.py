from service.contextmanager import session_scope
from service.getperson import GetPerson
from service.getportfolio import GetPortfolio
from domain.tabledef import BoughtCryptoStock, CryptoStock
from domain.tradingexceptions import NoStocksInPortfolioError
import datetime


class GetTransactions:

    def __init__(self, phone="", person=""):
        if not person:
            self.person = GetPerson(number=phone).get()
        else:
            self.person = person

    def get(self):

        portfolio = GetPortfolio(self.person).get()

        with session_scope() as session:
            transactions = session.query(BoughtCryptoStock).filter_by(portfolio_id=portfolio.id).all()

        if transactions is None:
            raise NoStocksInPortfolioError

        clean_transactions = []
        for t in transactions:

            with session_scope() as session:
                coin = session.query(CryptoStock).filter_by(id=t.crypto_stock_id).first()

            clean_transactions.append([coin, t])

        clean_transactions = sorted(clean_transactions, key=lambda item: item[1].created_at)
        return clean_transactions

    def print(self, transactions):

        nice_string = self.person.name+"'s *BUY TRANSACTION HISTORY*\n"

        index = 1
        for t in transactions:

            coin = t[0]
            bought_crypto = t[1]
            at_price = str(bought_crypto.at_price)
            fiat = str(bought_crypto.fiat_amount)
            buy_date = str(bought_crypto.created_at.strftime('%d-%m-%Y %H:%M:%S'))
            coin_amount = str(bought_crypto.coin_amount)

            nice_string += str(index)+". "+coin.name+" *@price:* "+at_price+" *@amount:* "+coin_amount+" *@total:* $"+fiat+" *@date:* "+buy_date+"\n"
            index += 1

        return nice_string
