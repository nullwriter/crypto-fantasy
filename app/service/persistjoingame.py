from domain.tabledef import GameRoundPlayer, Portfolio
from service.contextmanager import session_scope
from service.getgameround import GetGameRound


class PersistJoinGame:

    def __init__(self, game_round, player):
        self.game_round = game_round
        self.player = player

    def persist(self):

        game_round_player = GameRoundPlayer(
            person_id=self.player.id,
            game_round_id=self.game_round.id
        )

        with session_scope() as session:
            session.add(game_round_player)

        portfolio = Portfolio(
            game_round_player_id=game_round_player.id,
            fiat_amount=10000
        )

        with session_scope() as session:
            session.add(portfolio)
