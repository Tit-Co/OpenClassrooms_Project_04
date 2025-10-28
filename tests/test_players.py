import unittest
from src.chesstools.models import Player
from src.chesstools.controllers import PlayersManager


class TestPlayers(unittest.TestCase):

    def setUp(self):
        self.players = PlayersManager()
        self.player_1 = Player(name="Doe", first_name="John", identifier="JD123", birth_date="1990-01-01")
        self.player_2 = Player(name="Smith", first_name="Anna", identifier="AS456", birth_date="1992-05-05")

    def test_add_player(self):
        self.players.add_player(self.player_1)
        self.assertIn(self.player_1, self.players.data)

    def test_shuffle_players(self):
        self.players.add_player(self.player_1)
        self.players.add_player(self.player_2)
        before = self.players.data[:]
        self.players.shuffle()
        after = self.players.data

        self.assertCountEqual(before, after)


if __name__ == "__main__":

    unittest.main()
