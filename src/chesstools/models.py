from __future__ import annotations

# Standard library imports
import random
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import faker
# Third-party imports
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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

    def __rich_console__(self, console, *args, **kwargs):
        player_1, score_1, color_1 = self.match_tuple[0]
        player_2, score_2, color_2 = self.match_tuple[1]

        score_1_display = str(score_1) if score_1 is not None else 0
        score_2_display = str(score_2) if score_2 is not None else 0

        prefix = "[bold bright_white]┝╍ [/bold bright_white]"
        color_1_ = f"[bright_white]{color_1.upper()}[/bright_white]"
        color_2_ = f"[bright_white]{color_2.upper()}[/bright_white]"
        sep = " color : "
        score = " score : "

        table_1 = Table(show_header=False, border_style="black")
        table_1.add_column("Prefix", justify="center")
        table_1.add_column("Player", justify="center")
        table_1.add_column("Color 1", justify="center")
        table_1.add_column("Score Text", justify="center")
        table_1.add_column("Score 1", justify="center")

        table_1.add_row(prefix, player_1.__rich_console__(console), sep, color_1_, score, score_1_display)

        vs = "[bold yellow]VS[/bold yellow]"
        table_0 = Table(show_header=False, border_style="black")
        table_0.add_column("VS", justify="center")
        table_0.add_row(vs)

        table_2 = Table(show_header=False, border_style="black")
        table_2.add_column("Prefix", justify="center")
        table_2.add_column("Player", justify="center")
        table_2.add_column("Color 1", justify="center")
        table_2.add_column("Score Text", justify="center")
        table_2.add_column("Score 1", justify="center")

        table_2.add_row(prefix, player_2.__rich_console__(console), sep, color_2_, score, score_2_display)

        yield table_1
        yield table_0
        yield table_2
        yield "\n"

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

    def __rich_console__(self, console, *args, **kwargs):
        str_id = f"[bold red]{self.identifier}[/bold red]"
        sep = "[grey53] - [/grey53]"
        str_name = f"[bold blue]{self.first_name} {self.name.upper()} [/bold blue]"
        str_date = f"[grey53]born on {self.birth_date}[/grey53]"
        return str_id + sep + str_name + str_date

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

    def __rich_console__(self, console, *args, **kwargs):
        start = f"[dim grey58]{self.start_date} {self.start_time}[/dim grey58]" \
            if self.start_date and self.start_time else "Not started"
        end = f"[dim grey58]{self.end_date} {self.end_time}[/dim grey58]" \
            if self.end_date and self.end_time else "Not finished"

        prefix_dates = "[dim grey58] (from [/dim grey58]"
        sep = "[dim grey58] → [/dim grey58]"
        suffix_dates = "[dim grey58])[/dim grey58]"
        round_name = f"[bold bright_white]{self.round_name}[/bold bright_white]"

        round_str = round_name + prefix_dates + f"{start}" + sep + f"{end}" + suffix_dates

        if not self.matches:
            yield f"- The {self.round_name} has no matches yet."

        prefix = "[bold bright_white]- The [/bold bright_white]"
        middle = "[bold bright_white] has [/bold bright_white]"
        suffix = "[bold bright_white] matches:\n\n[/bold bright_white]"

        table_0 = Table(show_header=False, border_style="black")
        table_0.add_column("Header", justify="left")
        table_0.add_row(prefix + round_str + middle +
                        f"[bold bright_white]{len(self.matches)}[/bold bright_white]"
                        + suffix)
        for match in self.matches:
            table_0.add_row(match)
        yield table_0

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
    def __init__(self, name: str, place: str, start_date=None, end_date=None, description: str = "",
                 current_round: int = 1, rounds_number: int = NUMBER_OF_ROUNDS):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_number = rounds_number
        self.current_round = current_round
        self.rounds = []
        self.description = description
        self.players = []

    def __rich_console__(self, console, *args, **kwargs):
        rounds_str = ""

        name = f"[bold cyan]{self.name.upper()} [/bold cyan]"
        place_dates = (f"[white]({self.place}, {self.start_date} → {self.end_date}, "
                       f"currently in round {self.current_round} of {self.rounds_number} "
                       f"rounds, description : {self.description})[/white]")

        yield Panel(f"[cyan]├─   [/cyan] {name}" + f"{place_dates}", expand=False, border_style="cyan")

        if self.rounds:
            rounds_str = Panel("[bright_white]ALL ROUNDS[/bright_white]", expand=False)
            yield rounds_str

            for rnd in self.rounds:
                yield rnd

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

    def sort_players_by_score(self, verbose=False) -> None:
        """
        Method that sorts the players in Players object by their scores.
        Args:
            verbose (bool): Boolean flag to determine if scoreboard should be printed.
        """
        scores: dict[str, float] = defaultdict(float)

        player_by_id = {player.identifier: player for player in self.players}

        for rnd in (self.rounds or []):
            for match in rnd.matches:

                pairs = match.match_tuple

                for pair in pairs:
                    player_entry = pair[0]
                    raw_score = pair[1]
                    pid = player_entry.identifier
                    score = float(raw_score)
                    scores[pid] += score

            for player in self.players:
                scores.setdefault(player.identifier, 0.0)

            # debug : display the scoreboard if asked
            if verbose:
                print("⮞ Scoreboard :")
                for pid, score in sorted(scores.items(), key=lambda kv: kv[1], reverse=True):
                    player = player_by_id.get(pid)
                    label = f"{player.identifier} - {player.name} {player.first_name}" if player else pid
                    print(f"⮡ {label}: {score}")
                print("\n")

        sorted_players = sorted(self.players, key=lambda p: scores.get(p.identifier, 0.0), reverse=True)
        self.players[:] = sorted_players

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

        while players_list:
            first = players_list.pop(0)

            # seek a second player who has not played with the first one
            found_opponent = False
            for i, candidate in enumerate(players_list):
                if not self.match_already_played(first, candidate):
                    second = players_list.pop(i)
                    round_obj.matches.append(Match(first, second))
                    found_opponent = True
                    break

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
