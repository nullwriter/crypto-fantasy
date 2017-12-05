from sqlalchemy import desc

from service.getportfolio import GetPortfolio
from domain.tradingexceptions import NoStocksInPortfolioError, PlayerIsNotPartOfGameRoundError
from domain.tabledef import Leaderboard
from service.getgameround import GetGameRound
from service.getperson import GetPerson
from service.contextmanager import session_scope


class GetLeaderBoard:

    def __init__(self, game_round=None):
        if game_round is None:
            self.game_round = GetGameRound().get_current()
        else:
            self.game_round = game_round

    def get(self, game_round=None):

        if not game_round:
            game_round = self.game_round

        game_round_players = GetGameRound().get_all_game_round_players(game_round)
        get_portfolio = GetPortfolio()

        contestants = []
        for player in game_round_players:

            person = GetPerson().get_by_id(player.person_id)

            try:
                portfolio = get_portfolio.get_by_game_round_player(player)
            except PlayerIsNotPartOfGameRoundError:
                continue

            try:
                crypto_value = get_portfolio.get_crypto_value(portfolio)
            except NoStocksInPortfolioError:
                crypto_value = 0

            total_amount = float(portfolio.fiat_amount) + float(crypto_value)
            contestants.append([person.name, total_amount, portfolio])

        contestants = sorted(contestants, key=lambda item: item[1], reverse=True)
        return contestants

    def to_string(self):

        contestants = self.get()

        count = 1
        leaderboard_text = "*LEADERBOARD*\n"
        for contestant in contestants:
            total_amount_str = "%.2f" % contestant[1]
            leaderboard_text += str(count) + ". " + contestant[0] + " - $" + total_amount_str + "\n"
            count += 1

        if len(contestants) <= 0:
            leaderboard_text += "No players in current round.\n"

        leaderboard_text += "\nRound ends "+str(self.game_round.end.strftime('%b %d at %H:%M %p'))+"\n"

        prev_game = GetGameRound().get_previous()

        if prev_game:
            """
            1. Find leaderboard of previous game.
            2. If not saved, save them.
            3. Append to leaderboard string (top 3)
            """
            prev_leaderboard = self.get_previous_leaderboard(prev_game)

            if prev_leaderboard:
                leaderboard_text += "\n*_Previous top players:_*\n"
                count = 1
                for player in prev_leaderboard:
                    total_amount_str = "%.2f" % player.fiat_amount
                    leaderboard_text += str(count) + ". " + player.person_name + " - $" + total_amount_str + "\n"
                    count += 1
                    if count > 3:
                        break

        return leaderboard_text

    def get_previous_leaderboard(self, prev_game=None):

        if prev_game is None:
            prev_game = GetGameRound().get_previous()

        with session_scope() as session:
            prev_leaderboard = session.query(Leaderboard) \
                .filter_by(game_round_id=prev_game.id) \
                .order_by(desc(Leaderboard.fiat_amount)) \
                .all()

        if prev_leaderboard:
            return prev_leaderboard
        else:
            """
            Lets add it
            """
            contestants = self.get(prev_game)

            for player in contestants:
                name = player[0]
                portfolio = player[2]
                fiat_amount = player[1]

                leaderboard_unit = Leaderboard(
                    person_name=name,
                    portfolio_id=portfolio.id,
                    game_round_id=prev_game.id,
                    fiat_amount=fiat_amount
                )
                with session_scope() as session:
                    session.add(leaderboard_unit)

        with session_scope() as session:
            prev_leaderboard = session.query(Leaderboard) \
                .filter_by(game_round_id=prev_game.id) \
                .order_by(desc(Leaderboard.fiat_amount)) \
                .all()

        return prev_leaderboard
