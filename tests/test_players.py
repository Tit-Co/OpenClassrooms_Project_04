import unittest
from src.chesstools.models import Players, Player


class TestPlayers(unittest.TestCase):

    def setUp(self):
        self.players = Players()
        self.p1 = Player("Doe", "John", "JD123", "1990-01-01")
        self.p2 = Player("Smith", "Anna", "AS456", "1992-05-05")

    def test_add_player(self):
        self.players.add_player(self.p1)
        self.assertIn(self.p1, self.players)

    def test_shuffle_players(self):
        self.players.add_player(self.p1)
        self.players.add_player(self.p2)
        before = self.players[:]
        self.players.shuffle()
        after = self.players

        self.assertEqual(len(before), len(after))
        self.assertCountEqual(before, after)


if __name__ == "__main__":

    unittest.main()
