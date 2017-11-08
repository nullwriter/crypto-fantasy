from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime, timedelta


Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    phone_number = Column(String(200), nullable=False)
    authorized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class CryptoStock(Base):
    __tablename__ = 'crypto_stock'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=True)
    symbol = Column(String(50), nullable=False, unique=True)
    slug = Column(String(100), nullable=True)


class GameRound(Base):
    __tablename__ = 'game_round'

    id = Column(Integer, primary_key=True)
    start = Column(DateTime)
    end = Column(DateTime)


class GameRoundPlayer(Base):
    __tablename__ = 'game_round_player'

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))
    game_round_id = Column(Integer, ForeignKey('game_round.id'))


class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    game_round_player_id = Column(Integer, ForeignKey('game_round_player.id'))
    fiat_amount = Column(Float(2, asdecimal=True, decimal_return_scale=2), nullable=False)


class PortfolioStock(Base):
    """
    Will hold the accumulated stocks the portfolio has for easier retrieval
    """
    __tablename__ = 'portfolio_stocks'

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'))
    crypto_stock_id = Column(Integer, ForeignKey('crypto_stock.id'), nullable=False)
    coin_amount = Column(Float(8, asdecimal=True, decimal_return_scale=8), nullable=False)


class BoughtCryptoStock(Base):
    __tablename__ = 'bought_crypto_stock'

    id = Column(Integer, primary_key=True)
    crypto_stock_id = Column(Integer, ForeignKey('crypto_stock.id'), nullable=False)
    portfolio_id = Column(Integer, ForeignKey('portfolio.id'))
    at_price = Column(Float(2, asdecimal=True, decimal_return_scale=2), nullable=False)
    coin_amount = Column(Float(8, asdecimal=True, decimal_return_scale=8), nullable=False)
    fiat_amount = Column(Float(2, asdecimal=True, decimal_return_scale=2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)



