import unittest
from src.chesstools.models import Tournament, Round, Match, Player


class TestTournament(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player(name="Doe", first_name="John", birth_date="15/09/2000", identifier="JD1237")
        self.player_2 = Player(name="Smith", first_name="Anna", birth_date="21/05/1970", identifier="AS4568")

        self.tournament = Tournament(
            name="Test Tournament",
            place="Paris",
            start_date="2025-09-15",
            end_date="2025-09-17",
            description="Demo",
            rounds_number=2,
            current_round=1,
        )

        round_1 = Round("Round 1")
        match = Match(self.player_1, self.player_2)
        round_1.matches.append(match)

        self.tournament.rounds.append(round_1)

    def test_match_not_played_yet(self):
        player_3 = Player(name="Joe", first_name="Martin", birth_date="03/09/2005", identifier="po45823")
        self.assertFalse(self.tournament.match_already_played(self.player_1, player_3))

    def test_match_already_played_true(self):
        result = self.tournament.match_already_played(self.player_1, self.player_2)
        self.assertTrue(result)

    def test_match_already_played_false(self):
        player_3 = Player(name="Joe", first_name="Martin", birth_date="03/09/2005", identifier="po45823")
        result = self.tournament.match_already_played(self.player_1, player_3)
        self.assertFalse(result)


if __name__ == "__main__":

    unittest.main()
