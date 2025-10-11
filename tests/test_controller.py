import unittest
from src.chesstools.controllers import MainController
from src.chesstools.models import Tournament, Player, Players


class TestController(unittest.TestCase):

    def setUp(self):
        self.players = Players([
            Player(name="Doe", first_name="John", identifier="JD1", birth_date="1990-01-01"),
            Player(name="Smith", first_name="Anna", identifier="AS2", birth_date="1991-02-02"),
            Player(name="Brown", first_name="Charlie", identifier="CB3", birth_date="1992-03-03"),
            Player(name="Taylor", first_name="Emma", identifier="ET4", birth_date="1993-04-04"),
        ])

        self.tournament = Tournament(
            name="Test Tournament",
            place="Paris",
            start_date="2025-09-15",
            end_date="2025-09-17",
            players=self.players,
            description="Demo",
            rounds_number=2,
            current_round=1,
        )

        self.controller = MainController()
        self.controller.tournament_controller.current_tournament = self.tournament

    def test_create_first_round(self):
        self.controller.tournament_controller.current_tournament.create_round(1)

        self.assertEqual(len(self.tournament.rounds), 1)

        created_round = self.controller.tournament_controller.current_tournament.rounds[0]
        self.assertEqual(len(created_round.matches), 2)

        all_players_in_matches = []
        for match in created_round.matches:
            all_players_in_matches.append(match.match_tuple[0][0])
            all_players_in_matches.append(match.match_tuple[1][0])

        self.assertCountEqual(all_players_in_matches, self.players)

    def test_create_second_round(self):

        self.controller.tournament_controller.current_tournament.create_round(1)

        self.players[0].score = 1  # John Doe
        self.players[1].score = 1  # Anna Smith
        self.players[2].score = 0  # Charlie Brown
        self.players[3].score = 0  # Emma Taylor

        self.controller.tournament_controller.current_tournament.create_round(2)

        self.assertEqual(len(self.tournament.rounds), 2)

        created_round = self.tournament.rounds[1]
        self.assertEqual(len(created_round.matches), 2)

        all_players_in_matches = []
        for match in created_round.matches:
            all_players_in_matches.append(match.match_tuple[0][0])
            all_players_in_matches.append(match.match_tuple[1][0])

        self.assertCountEqual(all_players_in_matches, self.players)

    def test_no_repeat_matches_between_rounds(self):
        self.controller.tournament_controller.current_tournament.create_round(1)

        self.players[0].score = 1  # John
        self.players[1].score = 1  # Anna
        self.players[2].score = 0  # Charlie
        self.players[3].score = 0  # Emma

        round1_matches = self.controller.tournament_controller.current_tournament.rounds[0].matches
        played_pairs_round1 = set()
        for match in round1_matches:
            player_1 = match.match_tuple[0][0]
            player_2 = match.match_tuple[1][0]
            played_pairs_round1.add(frozenset([player_1, player_2]))

        self.controller.tournament_controller.current_tournament.create_round(2)

        round2_matches = self.controller.tournament_controller.current_tournament.rounds[1].matches
        played_pairs_round2 = set()
        for match in round2_matches:
            player_1 = match.match_tuple[0][0]
            player_2 = match.match_tuple[1][0]
            played_pairs_round2.add(frozenset([player_1, player_2]))

        self.assertTrue(played_pairs_round1.isdisjoint(played_pairs_round2))


if __name__ == "__main__":

    unittest.main()
