import traceback

from controller.registeraction import RegisterAction
from service.getcryptocoin import GetCryptoCoin
from controller.buyaction import BuyAction
from service.getgameround import GetGameRound
from controller.joingameaction import JoinGameAction
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

        help_str = "\nWelcome to the *Crypto Fantasy Trading Bot*!\n\n"\
                   "The commands available: \n\n" \
                   "- *help* -> shows this help section \n" \
                   "- *tutorial* -> explains the game\n" \
                   "- *tick <symbol>* or *ticker <symbol>* -> shows the crypto price, if no symbol " \
                   "then shows top 10. example: tick btc \n" \
                   "- *top <number>* -> shows a list of the top crypto currencies. example: top 10\n" \
                   "- *buy <amount_usd> <symbol>* -> to buy a crypto currency. example: buy 1000 btc\n" \
                   "- *sell <amount_coin> <symbol>* -> to sell a crypto currency. example: sell 0.15 btc\n" \
                   "- *leaderboard* -> shows the top players\n" \
                   "- *join* or *play* -> to join the current game round\n" \
                   "- *portfolio* -> shows your portfolio\n" \
                   "- *register <name>* -> will register to be able to play\n\n"

        return help_str

    def do_tutorial(self, arg, phone=""):

        tutorial_str = "Each player competes against all the others to try to create the best portfolio and make the most money.  " \
                       "The game starts at 8a.m. each day, and each player gets $10,000 of play money to work with.\n\n" \
                       "" \
                       "Over the course of the day, players buy and sell cryptocurrencies.  " \
                       "You can buy all the cryptocurrencies supported by the major exchanges. " \
                       "You make money when your picks go up and you lose money when they go down.\n " \
                       "So buy low and sell high!  After 24 hours, the game ends.\n\n"

        tutorial_str += "Here's what I suggest to you. \n\n Play a round right now!  First, type register <name> to be part of the system. " \
                        "Then, type join to enter the current round. After type portfolio to see your holdings. \n\n" \
                        "If you just started, it should be $10,000, all in USD.  Next, type buy 2000 BTC to get yourself a bitcoin position. " \
                        "Then type portfolio again to verify that you're now the proud owner of $2,000 worth of pretend BTC.\n" \
                        "Type sell .01 BTC to partially exit your BTC position, then check your holdings again with portfolio.  "

        return tutorial_str

    def do_info(self, arg, phone=""):
        try:
            return self.get_crypto_api.get_coin(symbol=arg)
        except Exception as e:
            return str(e)

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
        except Exception as e:
            return "Something went wrong..."+str(e)

    def do_leaderboard(self, arg, phone=""):
        try:
            return GetLeaderBoard().to_string()
        except NoPlayersInCurrentGameRoundError as e:
            return e.msg
        except Exception as e:
            print(traceback.format_exc())
            return "Something went wrong..."+str(e)

    def do_join(self, arg, phone=""):
        return self.do_play(arg, phone)

    def do_play(self, arg, phone=""):
        try:
            JoinGameAction(phone).join()
            return "Joined current round"
        except PlayerIsAlreadyInGameRoundError as e:
            return e.msg
        except Exception as e:
            print(traceback.format_exc())
            return "Something went wrong..."+str(e)

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
        except Exception as e:
            print(traceback.format_exc())
            return "Something went wrong..."+str(e)

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
        except Exception as e:
            print(traceback.format_exc())
            return "Something went wrong..." + str(e)

    def do_register(self, arg, phone=""):
        try:
            register_action = RegisterAction(phone=phone, name=arg)
            return register_action.persist()
        except YouAreAlreadyRegisteredError as e:
            return e.msg
        except Exception as e:
            return str(e)

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
        except Exception as e:
            return "Something went wrong..." + str(e)


    def do_say(self, arg, phone=""):
        return arg


def call_func(name, from_number, participant):

    wb = WhatsappBot()

    if participant is not None and "@" in participant:
        parts_sender = participant.split("@")
        sender = parts_sender[0]
    else:
        sender = from_number

    methods = {
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
        'transactions': wb.do_transactions
    }

    method_name = strip_args(name)
    args = get_args(method_name, name)

    if method_name.lower() not in methods:
        return False

    method = methods.get(method_name.lower())

    message_return = method(args, sender)
    return message_return


def strip_args(command):
    parts = command.split()
    return parts[0]


def get_args(command, fullstring):
    return fullstring.replace(command, '').strip()
