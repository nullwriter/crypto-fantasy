from service.getperson import GetPerson
from service.getgameround import GetGameRound
from domain.tradingexceptions import PlayerIsAlreadyInGameRoundError
from service.persistjoingame import PersistJoinGame


class JoinGameAction:

    def __init__(self, player="584142534221"):
        self.person = GetPerson(number=player).get()

    def join(self):
        """
        Things to do:
            1. Check current active round
            2. Check if user is in current round
            3. Add if not in round
            4. Create new portfolio with round_id
        """

        get_game_round = GetGameRound()
        active_round = get_game_round.get_current()

        if get_game_round.is_player_in_round(active_round, self.person):
            raise PlayerIsAlreadyInGameRoundError

        PersistJoinGame(active_round, self.person).persist()
