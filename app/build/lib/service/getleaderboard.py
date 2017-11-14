from service.getportfolio import GetPortfolio
from domain.tradingexceptions import NoStocksInPortfolioError
from service.getgameround import GetGameRound
from service.getperson import GetPerson


class GetLeaderBoard:

    def __init__(self):
        pass

    def to_string(self):

        """
        1. Get players of current round
        2. Get portfolios of players
        3. Order by descending
        """
        current_game = GetGameRound().get_current()
        game_round_players = GetGameRound().get_all_game_round_players(current_game)

        get_portfolio = GetPortfolio()

        contestants = []
        for player in game_round_players:

            person = GetPerson().get_by_id(player.person_id)
            portfolio = get_portfolio.get_by_game_round_player(player)

            try:
                crypto_value = get_portfolio.get_crypto_value(portfolio)
            except NoStocksInPortfolioError:
                crypto_value = 0

            total_amount = float(portfolio.fiat_amount) + float(crypto_value)
            contestants.append([person.name, total_amount])

        contestants = sorted(contestants, key=lambda item: item[1], reverse=True)

        count = 1
        leaderboard_text = "*LEADERBOARD*\n"
        for contestant in contestants:
            total_amount_str = "%.2f" % contestant[1]
            leaderboard_text += str(count) + ". " + contestant[0] + " - $" + total_amount_str + "\n"
            count += 1

        return leaderboard_text


