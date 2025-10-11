import unittest
from src.chesstools.models import Players, Player


class TestPlayers(unittest.TestCase):

    def setUp(self):
        self.players = Players()
        self.player_1 = Player(name="Doe", first_name="John", identifier="JD123", birth_date="1990-01-01")
        self.player_2 = Player(name="Smith", first_name="Anna", identifier="AS456", birth_date="1992-05-05")

    def test_add_player(self):
        self.players.add_player(self.player_1)
        self.assertIn(self.player_1, self.players)

    def test_shuffle_players(self):
        self.players.add_player(self.player_1)
        self.players.add_player(self.player_2)
        before = self.players[:]
        self.players.shuffle()
        after = self.players

        self.assertCountEqual(before, after)


if __name__ == "__main__":

    unittest.main()
