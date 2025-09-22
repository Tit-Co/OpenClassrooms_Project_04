import unittest
from src.chesstools.models import Tournament, Round, Match, Player, Players


class TestTournament(unittest.TestCase):

    def setUp(self):
        self.p1 = Player("Doe", "John", "15/09/2000", "JD1237")
        self.p2 = Player("Smith", "Anna", "21/05/1970", "AS4568")

        self.tournament = Tournament(
            name="Test Tournament",
            place="Paris",
            start_date="2025-09-15",
            end_date="2025-09-17",
            players=Players([self.p1, self.p2]),
            description="Demo",
            rounds_number=2,
            current_round=1,
        )

        round1 = Round("Round 1")
        match = Match(self.p1, self.p2)
        round1.matches.append(match)

        self.tournament.rounds.append(round1)

    def test_match_not_played_yet(self):
        p3 = Player("Joe", "Martin", "03/09/2005", "po45823")
        self.assertFalse(self.tournament.match_already_played(self.p1, p3))

    def test_match_already_played_true(self):
        result = self.tournament.match_already_played(self.p1, self.p2)
        self.assertTrue(result)

    def test_match_already_played_false(self):
        p3 = Player("Joe", "Martin", "03/09/2005", "po45823")
        result = self.tournament.match_already_played(self.p1, p3)
        self.assertFalse(result)


if __name__ == "__main__":

    unittest.main()
