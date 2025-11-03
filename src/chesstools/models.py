from __future__ import annotations

# Standard library imports
import random
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import faker
# Third-party imports
from rich.console import Console

# Initialize Console
console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",  # active la palette complète
    width=200
)

fake = faker.Faker()
NUMBER_OF_ROUNDS = 4
TOURNAMENT_FOLDER = Path("./data/tournaments/")
TOURNAMENTS_DATA_JSON = TOURNAMENT_FOLDER / Path("./tournaments.json")
PLAYERS_DATA_JSON = TOURNAMENT_FOLDER / Path("./players.json")


class Match:
    def __init__(self, player_1: Player, player_2: Player, score_1: float = 0.0, score_2: float = 0.0):
        match_1 = (player_1, score_1, "⚪")
        match_2 = (player_2, score_2, "⚫")
        if random.choice([True, False]):
            self.match_tuple: tuple[tuple[Player, float, str], tuple[Player, float, str]] = (
                match_1,
                match_2,
            )
        else:
            self.match_tuple = (match_2, match_1)

    def __iter__(self):
        return iter(self.match_tuple)

    def __str__(self):
        player_1, score_1, color_1 = self.match_tuple[0]
        player_2, score_2, color_2 = self.match_tuple[1]

        score_1_display = score_1 if score_1 is not None else 0
        score_2_display = score_2 if score_2 is not None else 0

        prefix = "┝╍ "
        color_1_ = f"{color_1.upper()}"
        color_2_ = f"{color_2.upper()}"
        sep = " - "
        score = " - score: "
        line1 = prefix + f"{player_1}" + sep + color_1_ + score + f"{score_1_display}\n"
        bar = "│ "
        vs = "VS\n"
        line2 = prefix + f"{player_2}" + sep + color_2_ + score + f"{score_2_display}\n"

        return line1 + bar + vs + line2

    def __repr__(self):
        return str(self.match_tuple)

    def set_colors(self, color_1: str, color_2: str) -> None:
        """
        Method that sets the players color in the match.
        Args:
            color_1 (str): The color 1.
            color_2 (str): The color 2.
        """
        p1, s1, _ = self.match_tuple[0]
        p2, s2, _ = self.match_tuple[1]
        self.match_tuple = (
            (p1, s1, color_1),
            (p2, s2, color_2),
        )

    def convert_to_dict(self) -> dict[str, dict[str, str | float]]:
        """
        Method that converts the match tuple to a dictionary.
        Returns:

        """
        player_1, score_1, color_1 = self.match_tuple[0]
        player_2, score_2, color_2 = self.match_tuple[1]
        return {
            "player1": {
                "identifier": player_1.identifier,
                "score": score_1,
                "color": color_1,
            },
            "player2": {
                "identifier": player_2.identifier,
                "score": score_2,
                "color": color_2,
            }
        }


class Player:
    def __init__(self, name: str, first_name: str, birth_date: str, identifier: str):
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.identifier = identifier

    def __str__(self):
        str_id = f"{self.identifier}"
        sep = " - "
        str_name = f"{self.first_name} {self.name.upper()} "
        str_date = f"born on {self.birth_date}"
        return str_id + sep + str_name + str_date

    def __repr__(self):
        return str(self)

    def convert_to_dict(self) -> dict[str, str]:
        """
        Method that converts the player's data to a dictionary.
        Returns: The dictionary of the player's data.
        """
        return {"name": self.name,
                "first_name": self.first_name,
                "birth_date": self.birth_date}


class Round:
    def __init__(self, round_name):
        self.round_name = round_name
        self.matches = []
        self.start_date = None
        self.start_time = None
        self.end_date = None
        self.end_time = None

    def __str__(self):
        start = f"{self.start_date} {self.start_time}" \
            if self.start_date and self.start_time else "Not started"
        end = f"{self.end_date} {self.end_time}" \
            if self.end_date and self.end_time else "Not finished"

        prefix_dates = " (from "
        sep = " → "
        suffix_dates = ")"
        round_name = f"{self.round_name}"

        round_str = round_name + prefix_dates + f"{start}" + sep + f"{end}" + suffix_dates

        if not self.matches:
            return f"- The {self.round_name} has no matches yet."

        matches_str = ""
        for match in self.matches:
            matches_str += f"{match}\n"

        prefix = "- The "
        middle = " has "
        suffix = " matches:\n\n"
        return prefix + f"{round_str}" + middle + f"{len(self.matches)}" + suffix + f"{matches_str}"

    def __repr__(self):
        return str(self)

    def set_start_date(self) -> None:
        """
        Method that sets the start date of the round.
        """
        now = datetime.now()
        self.start_date = now.strftime("%d/%m/%Y")
        self.start_time = now.strftime("%H:%M:%S")

    def set_end_date(self) -> None:
        """
        Method that sets the end date of the round.
        """
        now = datetime.now()
        self.end_date = now.strftime("%d/%m/%Y")
        self.end_time = now.strftime("%H:%M:%S")

    @staticmethod
    def get_random_scores() -> tuple[float, float]:
        """
        Method that gets a random score between 0, 1 and 0.5. Used only for testing purposes.
        Returns:
            A random score in a tuple.
        """
        scenario = random.randint(0, 2)
        if scenario == 0:
            return 1, 0
        if scenario == 1:
            return 0, 1
        return 0.5, 0.5

    def convert_to_dict(self) -> dict[str, dict[str, dict] | str | datetime]:
        """
        Method that converts the round's data to a dictionary.
        Returns: The dictionary of the round's data.
        """
        return {
            "round_name": self.round_name,
            "start_date": self.start_date,
            "start_time": self.start_time,
            "end_date": self.end_date,
            "end_time": self.end_time,
            "matches": {f"match_{i+1}": match.convert_to_dict() for i, match in enumerate(self.matches)}
        }


class Tournament:
    def __init__(self, name: str, place: str, rounds_number: int, start_date=None, end_date=None,
                 description: str = "", current_round: int = 1):
        self.name = name
        self.place = place
        self.rounds_number = rounds_number
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.current_round = current_round
        self.rounds = []
        self.players = []

    def __str__(self):
        rounds_str = ""
        if self.rounds:
            prefix = "│"
            prefix_rnd = "   │"
            rounds_str = prefix + "   ┌ ALL ROUNDS :\n"
            for rnd in self.rounds:
                for line in str(rnd).splitlines():
                    rounds_str += prefix + prefix_rnd + f" {line}\n"
            suffix = "   └──────────────\n"
            rounds_str += prefix + suffix

        name = f"{self.name.upper()} "
        place_dates = (f"({self.place}, {self.start_date} → {self.end_date} currently in round "
                       f"{self.current_round} of {self.rounds_number} rounds, description : {self.description})\n")
        return name + place_dates + f"{rounds_str}"

    def __repr__(self):
        return str(self)

    def is_completed(self) -> bool:
        """
        Methods that checks if the round is completed.
        Returns:
            True if the round is completed. False otherwise.
        """
        if self.current_round == 4:
            if self.rounds[3].end_date:
                return True
            return False
        return False

    def add_players(self, players: Iterable[Player]) -> None:
        """
        Method that copies the players object and adds them to the tournament Players object.
        Args:
            players (Players): Players object.
        """
        for player in players:
            self.players.append(player)

    def add_round(self, tournament_round: Round) -> None:
        """
        Method that adds a round to the tournament Rounds object.
        Args:
            tournament_round (Round): Round object.
        """
        self.rounds.append(tournament_round)

    @staticmethod
    def compute_player_scores(tournament) -> tuple[dict[str, float], dict[str, Player]]:
        """
        Method that computes the player scores for all players in the tournament.
        Args:
            tournament (Tournament): Tournament object.

        Returns:
            A score associated to player's id.
        """
        id_to_player = {player.identifier: player for player in tournament.players}
        # init scores to 0.0
        scores = {player_id: 0.0 for player_id in id_to_player.keys()}

        for rnd in getattr(tournament, "rounds", []):
            for match in getattr(rnd, "matches", []) or []:

                player_1_obj, score_1, _ = match.match_tuple[0]
                player_2_obj, score_2, _ = match.match_tuple[1]

                score_1_val = float(score_1) if score_1 is not None else 0.0
                score_2_val = float(score_2) if score_2 is not None else 0.0

                scores[player_1_obj.identifier] = scores.get(player_1_obj.identifier, 0.0) + score_1_val
                scores[player_2_obj.identifier] = scores.get(player_2_obj.identifier, 0.0) + score_2_val

        return scores, id_to_player

    def sort_players_by_score(self) -> list:
        """
        Method that sorts the players in Players object by their scores.
        Returns:
            A sorted list of players.
        """
        scores = {}
        for rnd in (self.rounds or []):
            for match in rnd.matches:
                for player, raw_score, _ in match.match_tuple:
                    pid = player.identifier
                    scores[pid] = scores.get(pid, 0.0) + float(raw_score)

        ordered = sorted(self.players, key=lambda p: scores.get(p.identifier, 0.0), reverse=True)

        self.players[:] = ordered

        return ordered

    def create_round(self, round_number: int, players: list) -> None:
        """
        Method that creates a round object.
        Args:
            round_number (int): The round number.
            players (list): A list of Player objects.
        """
        round_obj = Round(f"Round {round_number}")

        self.create_matches(players, round_obj)
        round_obj.set_start_date()

        self.rounds.append(round_obj)

    def create_matches(self, players: list, round_obj: Round) -> None:
        """
        Creates matches for a given round, ensuring players haven't played each other before.

        Args:
            players (Players): The players participating in the tournament.
            round_obj (Round): The round object to populate with matches.
        """
        players_list = players.copy()
        round_obj.matches = []

        while len(players_list) >= 2:
            first = players_list.pop(0)

            # seek a second player who has not played with the first one near the first one score
            found_opponent = False
            best_candidate_index = None
            best_score_diff = float(1000)

            for i, candidate in enumerate(players_list):
                if not self.match_already_played(first, candidate):
                    # Seek a candidate with the nearest score
                    diff = abs(getattr(first, "score", 0.0) - getattr(candidate, "score", 0.0))
                    if diff < best_score_diff:
                        best_score_diff = diff
                        best_candidate_index = i

            # found
            if best_candidate_index is not None:
                second = players_list.pop(best_candidate_index)
                round_obj.matches.append(Match(first, second))
                found_opponent = True

            # If no suitable candidate found, pair with the first available
            if not found_opponent and players_list:
                second = players_list.pop(0)
                round_obj.matches.append(Match(first, second))

    def match_already_played(self, player_1: Player, player_2: Player) -> bool:
        """
        Method that checks if two players have already faced each other in this tournament.
        Args:
            player_1 (Player): Player 1 object.
            player_2 (Player): Player 2 object.

        Returns:
            A boolean indicating if the player 1 has already played with player 2.
        """
        pair_to_check = frozenset([player_1.identifier, player_2.identifier])

        for rnd in self.rounds:
            for match in rnd.matches:
                match_player_1 = match.match_tuple[0][0].identifier
                match_player_2 = match.match_tuple[1][0].identifier
                existing_pair = frozenset([match_player_1, match_player_2])

                if pair_to_check == existing_pair:
                    return True
        return False

    def convert_to_dict(self) -> dict[str, str | datetime | dict[str, dict] | dict[Any, Any]]:
        """
        Method that converts the player's data to a dictionary.
        Returns: The dictionary of the player's data.
        """
        return {
            "place": self.place,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "current_round": self.current_round,
            "rounds_number": self.rounds_number,
            "players": {str(player.identifier): player.convert_to_dict() for player in self.players},
            "rounds": {rnd.round_name: rnd.convert_to_dict() for rnd in self.rounds}
        }
