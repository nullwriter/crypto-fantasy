from controller import BOT_ORM_SESSION, BOT_ENGINE
from domain.tabledef import *
from service.getcryptocoin import GetCryptoCoin
import pandas as pd
from datetime import datetime, date, time, timedelta


class DatabaseOrm:

    def __init__(self):
        self.session = BOT_ORM_SESSION()

    def initialize(self):
        """
        Creates the database and also adds the initial data for system to work (coins, admin account)
        """
        Base.metadata.create_all(BOT_ENGINE)
        self.add_initial_data()

    def add_initial_data(self):
        """
        Tables with necessary initial data are:
            1. CryptoStock
            2. GameRound
            3. Person
        """
        if self.session.query(CryptoStock).first() is None:
            print(">>>> Adding crypto coins to database")
            self.add_crypto_coins_data()

        if self.session.query(GameRound).first() is None:
            print(">>>> Adding game rounds to database")
            self.add_game_rounds()

        if self.session.query(Person).first() is None:
            print(">>>> Adding test person to database")
            self.add_test_user()

    def add_game_rounds(self, days_length=7):

        dates = pd.date_range('2017-11-06 08:00:00', periods=365, freq='D')

        index = 1
        for day in dates:
            if 0 == index % days_length or index == 1:
                start = str(day)
                next_day = day + timedelta(days=days_length)

                """[0] has the day, [1] has the hour 08:00:00"""
                element = str(next_day).split()
                end = element[0]+" 07:59:59"

                dt_start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
                dt_end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")

                game_round = GameRound(
                    start=dt_start,
                    end=dt_end
                )
                self.session.add(game_round)
            index += 1

        self.session.commit()

    def add_test_user(self):
        person = Person(
            name="Christian Feo",
            phone_number="584142534221",
            authorized=True
        )

        self.session.add(person)
        self.session.commit()

    def add_crypto_coins_data(self):
        gcc = GetCryptoCoin()

        coins = gcc.get_all_coins(limit=100)
        for coin in coins:
            crypto_stock = CryptoStock(
                name=coin['name'],
                symbol=coin['symbol'],
                slug=coin['id']
            )
            self.session.add(crypto_stock)

        self.session.commit()
