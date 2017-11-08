import cmd, sys
from service.getcryptocoin import GetCryptoCoin
from controller.buyaction import BuyAction
from service.getgameround import GetGameRound
from controller.joingameaction import JoinGameAction
from service.getportfolio import GetPortfolio
from service.getperson import GetPerson
from controller.sellaction import SellAction
from service.getleaderboard import GetLeaderBoard


class ShellBot(cmd.Cmd):
    intro = 'Welcome to the Crypto Fantasy shell.   Type help or ? to list commands.\n'
    prompt = '(crypto_fantasy) '
    file = None

    def __init__(self):
        super().__init__()
        self.get_crypto_api = GetCryptoCoin()

    def default(self, arg):
        print("Sorry, I'm not sure what you mean by '"+arg+"'. Type ? or help for a list of commands.")

    def do_help(self, arg):

        help_str = "\n\nThe commands available: \n\n" \
               "- ? or help -> shows this help section \n" \
               "- bye -> exits the program\n" \
               "- tick <symbol> or ticker <symbol> -> shows the crypto price, if no symbol " \
               "then shows top 10. example: tick btc \n" \
               "- top <number> -> shows a list of the top crypto currencies. example: top 10\n" \
               "- buy <amount_usd> <symbol> -> to buy a crypto currency. example: buy 1000 btc\n" \
               "- sell <amount_coin> <symbol> -> to sell a crypto currency. example: sell 0.15 btc\n" \
               "- leaderboard -> shows the top players\n\n"

        print(help_str)

    def do_bye(self, arg):
        print("Goodbye :)")
        exit(1)

    def do_info(self, arg):
        try:
            print(self.get_crypto_api.get_coin(symbol=arg))
        except Exception as e:
            print(e.msg)

    def do_tick(self, arg):
        self.do_ticker(arg)

    def do_ticker(self, arg):
        if not arg:
            print(self.get_crypto_api.get_top_coins())
        else:
            print(self.get_crypto_api.get_coin_price(symbol=arg))

    def do_top(self, arg):
        if not arg or not arg.isdigit():
            print("You need to provide a number. E.g. top 10")
        else:
            print(self.get_crypto_api.get_top_coins(limit=arg))

    def do_test(self, arg):
        try:
            print(GetGameRound().get_current())
        except Exception as e:
            print(e.msg)

    def do_portfolio(self, arg):
        try:
            person = GetPerson(number="584142534221").get()
            portfolio = GetPortfolio(person).get()
            portfolio_string = GetPortfolio(person).print(portfolio)
            print(portfolio_string)
        except Exception as e:
            print(e.msg)

    def do_leaderboard(self, arg):
        try:
            GetLeaderBoard().print()
        except Exception as e:
            print(e.msg)

    def do_join(self, arg):
        self.do_play(arg)

    def do_play(self, arg):
        try:
            JoinGameAction().join()
            print("Joined current round")
        except Exception as e:
            print(e.msg)

    def do_buy(self, arg):
        args = arg.split()

        try:
            buy_action = BuyAction(symbol=args[1], fiat_amount=args[0])
            buy_action.persist()
        except IndexError:
            print("Wrong input. Please write amount in USD and the crypto symbol. Example: buy 1000 btc")
        except Exception as e:
            print(e.msg)

    def do_sell(self, arg):
        args = arg.split()

        try:
            sell_action = SellAction(symbol=args[1], coin_amount=args[0])
            sell_action.persist()
        except IndexError:
            print("Wrong input. Please write amount in Coins and the crypto symbol. Example: sell 0.15 btc")
        except Exception as e:
            print(e.msg)
