
class Error(Exception):
    pass


class NoCrytoCurrencyFoundError(Error):
    def __init__(self):
        self.msg = "That Crypto Currency was not found"


class CryptoCurrencyNotFoundInPortfolio(Error):
    def __init__(self):
        self.msg = "You currently don't own that Crypto Currency"


class NoPersonWasFoundError(Error):
    def __init__(self):
        self.msg = "There was no person found to make this transaction"


class NoGameRoundFoundError(Error):
    def __init__(self):
        self.msg = "There was no GameRound found for the specified date"


class PlayerIsAlreadyInGameRoundError(Error):
    def __init__(self):
        self.msg = "Player is already part of the game round"


class PlayerIsNotPartOfGameRoundError(Error):
    def __init__(self):
        self.msg = "Player is not part of current game round"


class NoStocksInPortfolioError(Error):
    def __init__(self):
        self.msg = "You currently have no crypto coins in your portfolio"


class NotEnoughMoneyError(Error):
    def __init__(self):
        self.msg = "Not enough money for current transaction"


class NotEnoughCryptoCoinError(Error):
    def __int__(self):
        self.msg = "Not enough crypto coins or usd in your portfolio for current transaction"


class NoCurrentPlayersInRound(Error):
    def __init__(self):
        self.msg = "There currently aren't any players in the game round :(. Type play or join to start"


class YouAreAlreadyRegisteredError(Error):
    def __init__(self):
        self.msg = "You are already registered :). Write *join* or *play* to enter the current round."


class NoPlayersInCurrentGameRoundError(Error):
    def __init__(self):
        self.msg = "No players in current game round."
