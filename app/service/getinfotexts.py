

class GetInfoTexts:

    @staticmethod
    def get_help():
        help_str = "\nWelcome to the *Crypto Fantasy Trading Bot*!\n\n" \
                   "The commands available: \n\n" \
                   "- *help* -> shows this help section \n" \
                   "- *tutorial* -> explains the game\n" \
                   "- *tick <symbol>* or *ticker <symbol>* -> shows the crypto price, if no symbol " \
                   "then shows top 10. example: tick btc \n" \
                   "- *top <number>* -> shows a list of the top crypto currencies. example: top 10\n" \
                   "- *buy <amount_usd> <symbol>* -> to buy a crypto currency. example: buy 1000 btc\n" \
                   "- *sell <amount_coin> <symbol>* or *sell $<amount_usd> <symbol>* -> to sell a crypto currency." \
                   " example: sell 0.15 btc or sell 1500$ btc\n" \
                   "- *leaderboard* -> shows the top players\n" \
                   "- *join* or *play* -> to join the current game round\n" \
                   "- *portfolio* -> shows your portfolio\n" \
                   "- *register <name>* -> will register to be able to play\n" \
                   "- *transactions* -> will show your buy transaction history\n\n"
        return help_str

    @staticmethod
    def get_tutorial():
        tutorial_str = "Each player competes against all the others to try to create the best portfolio and make the" \
                       " most money.  " \
                       "The game starts at 8a.m. each day, and each player gets $10,000 of play money to" \
                       " work with.\n\n" \
                       "" \
                       "Over the course of the week, players buy and sell cryptocurrencies.  " \
                       "You can buy all the cryptocurrencies supported by the major exchanges. " \
                       "You make money when your picks go up and you lose money when they go down.\n " \
                       "So buy low and sell high!  After a week, the game ends.\n\n"

        tutorial_str += "Here's what I suggest to you. \n\n Play a round right now!  First, type register <name> to" \
                        " be part of the system. " \
                        "Then, type join to enter the current round. After type portfolio to see your holdings. \n\n" \
                        "If you just started, it should be $10,000, all in USD.  Next, type buy 2000 BTC to get" \
                        " yourself a bitcoin position. " \
                        "Then type portfolio again to verify that you're now the proud owner of $2,000 worth of" \
                        " pretend BTC.\n" \
                        "Type sell 0.01 BTC to partially exit your BTC position, then check your holdings again with" \
                        " portfolio.  "

        return tutorial_str