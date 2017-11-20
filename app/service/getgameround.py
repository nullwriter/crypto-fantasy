from datetime import datetime
from domain.tabledef import GameRound, GameRoundPlayer
from domain.tradingexceptions import NoGameRoundFoundError, PlayerIsNotPartOfGameRoundError, NoPlayersInCurrentGameRoundError
from service.contextmanager import session_scope


class GetGameRound:

    def __init__(self):
        pass

    def get_current(self):
        now = datetime.now()

        with session_scope() as session:
            game_round = session.query(GameRound).filter(GameRound.start <= now, GameRound.end > now).first()

        if game_round is None:
            raise NoGameRoundFoundError

        return game_round

    def get_previous(self):
        current_game = self.get_current()
        prev_id = current_game.id - 1

        if prev_id < 1:
            return False

        with session_scope() as session:
            prev_game = session.query(GameRound).filter_by(id=prev_id).first()

        print("previous game = "+str(prev_game))

        return prev_game

    def is_player_in_round(self, game_round, player):

        with session_scope() as session:
            game_round_player = session.query(GameRoundPlayer).filter_by(
                person_id=player.id,
                game_round_id=game_round.id).first()

        return game_round_player is not None

    def get_game_round_player(self, game_round, player):

        with session_scope() as session:
            game_round_player = session.query(GameRoundPlayer).filter_by(
                person_id=player.id,
                game_round_id=game_round.id).first()

        if game_round_player is None:
            raise PlayerIsNotPartOfGameRoundError

        return game_round_player

    def get_all_game_round_players(self, game_round):

        with session_scope() as session:
            game_round_players = session.query(GameRoundPlayer).filter_by(
                game_round_id=game_round.id).all()

        if game_round_players is None:
            raise NoPlayersInCurrentGameRoundError

        return game_round_players
