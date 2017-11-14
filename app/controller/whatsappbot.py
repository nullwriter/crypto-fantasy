import traceback
import random
import re
from controller.registeraction import RegisterAction
from service.getcryptocoin import GetCryptoCoin
from controller.buyaction import BuyAction
from service.getgameround import GetGameRound
from controller.joingameaction import JoinGameAction
from service.getinfotexts import GetInfoTexts
from service.getportfolio import GetPortfolio
from service.getperson import GetPerson
from controller.sellaction import SellAction
from service.getleaderboard import GetLeaderBoard
from domain.tradingexceptions import NoCrytoCurrencyFoundError, PlayerIsAlreadyInGameRoundError, \
    PlayerIsNotPartOfGameRoundError, NoPlayersInCurrentGameRoundError, NotEnoughMoneyError, NotEnoughCryptoCoinError, \
    YouAreAlreadyRegisteredError, NoPersonWasFoundError, NoStocksInPortfolioError
from service.gettransactions import GetTransactions

ADMIN_USER = "59414253421"


class WhatsappBot:

    def __init__(self):
        self.get_crypto_api = GetCryptoCoin()

    def default(self, arg, phone=""):
        return "Sorry, I'm not sure what you mean by '"+arg+"'. Type help for a list of commands."

    def do_help(self, arg, phone=""):
        return GetInfoTexts().get_help()

    def do_tutorial(self, arg, phone=""):
        return GetInfoTexts().get_tutorial()

    def do_info(self, arg, phone=""):
        return self.get_crypto_api.get_coin(symbol=arg)

    def do_tick(self, arg, phone=""):
        return self.do_ticker(arg)

    def do_ticker(self, arg, phone=""):
        try:
            if not arg:
                return self.get_crypto_api.get_top_coins()
            else:
                return self.get_crypto_api.get_coin_price(symbol=arg)
        except NoCrytoCurrencyFoundError as e:
            return "Symbol: "+arg+". "+e.msg

    def do_top(self, arg, phone=""):
        if not arg or not arg.isdigit():
            return "You need to provide a number. E.g. top 10"
        else:
            return self.get_crypto_api.get_top_coins(limit=arg)

    def do_portfolio(self, arg, phone=""):
        try:
            person = GetPerson(number=phone).get()
            portfolio = GetPortfolio(person).get()
            portfolio_string = GetPortfolio(person).print(portfolio)
            return portfolio_string
        except PlayerIsNotPartOfGameRoundError as e:
            return e.msg

    def do_leaderboard(self, arg, phone=""):
        try:
            return GetLeaderBoard().to_string()
        except NoPlayersInCurrentGameRoundError as e:
            return e.msg

    def do_join(self, arg, phone=""):
        return self.do_play(arg, phone)

    def do_play(self, arg, phone=""):
        try:
            JoinGameAction(phone).join()
            return "Joined current round"
        except PlayerIsAlreadyInGameRoundError as e:
            return e.msg

    def do_buy(self, arg, phone=""):
        args = arg.split()

        try:
            buy_action = BuyAction(symbol=args[1], fiat_amount=args[0], player=phone)
            return buy_action.persist()
        except PlayerIsNotPartOfGameRoundError as e:
            return "Cannot do buy. "+e.msg
        except IndexError:
            return "Wrong input. Please write amount in USD and the crypto symbol. Example: buy 1000 btc"
        except NotEnoughMoneyError as e:
            return e.msg
        except NoCrytoCurrencyFoundError as e:
            return "Symbol: " + arg + ". " + e.msg

    def do_sell(self, arg, phone):
        args = arg.split()

        try:
            sell_action = SellAction(symbol=args[1], coin_amount=args[0], player=phone)
            return sell_action.persist()
        except PlayerIsNotPartOfGameRoundError as e:
            return "Cannot do sell. " + e.msg
        except NotEnoughCryptoCoinError:
            return "Not enough crypto coins available"
        except IndexError:
            return "Wrong input. Please write amount in Coins and the crypto symbol. " \
                   "Example: sell 0.15 btc or sell 1500$ btc"

    def do_register(self, arg, phone=""):
        try:
            register_action = RegisterAction(phone=phone, name=arg)
            return register_action.persist()
        except YouAreAlreadyRegisteredError as e:
            return e.msg

    def do_transactions(self, arg, phone=""):
        try:
            get_transactions = GetTransactions(phone=phone)
            transactions = get_transactions.get()
            return get_transactions.print(transactions)
        except NoPersonWasFoundError as e:
            return e.msg
        except NoStocksInPortfolioError as e:
            return e.msg
        except PlayerIsNotPartOfGameRoundError as e:
            return e.msg

    def do_hello(self, arg, phone=""):

        scripts = [
            "Hey, I'm back :)",
            "Hello hooman, whats up?",
            "Waddup dawg?",
            "Yo, we be here all day everyday",
            "Sup?",
            "I missed you guy(s).",
            "Hit me up, I'm ready"
        ]

        return random.choice(scripts)

    def do_say(self, arg, phone=""):
        return arg


class MethodCallInterface:

    def __init__(self):
        wb = WhatsappBot()

        self.methods = {
            'default': wb.default,
            'help': wb.do_help,
            'info': wb.do_info,
            'tick': wb.do_tick,
            'ticker': wb.do_tick,
            'precio': wb.do_tick,
            'top': wb.do_top,
            'buy': wb.do_buy,
            'sell': wb.do_sell,
            'leaderboard': wb.do_leaderboard,
            'portfolio': wb.do_portfolio,
            'join': wb.do_join,
            'play': wb.do_play,
            'say': wb.do_say,
            'register': wb.do_register,
            'tutorial': wb.do_tutorial,
            'transactions': wb.do_transactions,
            'botty': wb.do_hello,
            'hi': wb.do_hello
        }

    def resolve(self, message, from_number, participant):
        sender = self.get_recepient(participant, from_number)
        command = self.get_command(message)
        args = self.get_args(command, message)

        if command.lower() not in self.methods:
            return False

        bot_action = self.methods.get(command.lower())

        try:
            return bot_action(args, sender)
        except Exception as e:
            print(traceback.format_exc())
            return "Something went wrong..." + str(e)

    @staticmethod
    def get_command(message):
        parts = message.split()
        return re.sub('[^A-Za-z0-9]+', '', parts[0])

    @staticmethod
    def get_args(command, fullstring):
        return fullstring.replace(command, '').strip()

    @staticmethod
    def get_recepient(participant, from_number):
        if participant is not None and "@" in participant:
            parts_sender = participant.split("@")
            sender = parts_sender[0]
        else:
            sender = from_number

        return sender
