from __future__ import annotations

# Standard library imports
import json
import random
import string
import sys
from collections import UserList, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import faker
# Third-party imports
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


# Initialize Colorama
init(autoreset=True)

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

        prefix = Fore.WHITE + Style.BRIGHT + "┝╍ "
        color_1_ = Fore.WHITE + f"{color_1.upper()}"
        color_2_ = Fore.WHITE + f"{color_2.upper()}"
        sep = " - "
        score = " - score: "
        line1 = prefix + f"{player_1}" + sep + color_1_ + score + f"{score_1_display}\n"
        bar = "│ "
        vs = Fore.YELLOW + Style.DIM + "VS\n"
        line2 = prefix + f"{player_2}" + sep + color_2_ + score + f"{score_2_display}\n"

        return line1 + bar + vs + line2

    def __repr__(self):
        return str(self.match_tuple)

    def set_scores(self, player_1: Player, score_1: float, player_2: Player, score_2: float) -> None:
        """
        Method that sets the scores of the match.
        Args:
            player_1 (Player): The player 1 associated to score 1.
            score_1 (float): The score 1.
            player_2 (Player): The player 2 associated to score 2.
            score_2 (float): The score 2.
        """

        p1, s1, c1 = self.match_tuple[0]
        p2, s2, c2 = self.match_tuple[1]

        if p1 == player_1:
            self.match_tuple = (
                (p1, score_1, c1),
                (p2, score_2, c2),
            )
        elif p1 == player_2:
            self.match_tuple = (
                (p1, score_2, c1),
                (p2, score_1, c2),
            )
        else:
            print("Scores bug !")

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
        str_id = Fore.RED + Style.DIM + f"{self.identifier}"
        sep = Fore.WHITE + Style.NORMAL + " - "
        str_name = Fore.BLUE + Style.BRIGHT + f"{self.first_name} {self.name.upper()} "
        str_date = Fore.WHITE + Style.NORMAL + f"born on {self.birth_date}"
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

# @dataclass
# class Player:
#
#     name: str
#     birth_date: str
#
#     def __str__(self):
#         str_id = Fore.RED + Style.DIM + f"{self.identifier}"
#         sep = Fore.WHITE + Style.NORMAL + " - "
#         str_na = Fore.BLUE + Style.BRIGHT + f"{self.first_name} {self.name.upper()} "
#         str_da = Fore.WHITE + Style.NORMAL + f"born on {self.birth_date}"
#         return str_id + sep + str_na + str_da
#
#     def __repr__(self):
#         return str(self)

# player  = PLayer()
# player.__dict__

    # Create init without


class Players(UserList):
    def __init__(self, players=None):
        super().__init__(players or [])

    def __rich_console__(self, console, *args, **kwargs):
        header = Panel("ALL PLAYERS", border_style="bright_red", style="bright_red", expand=False)
        yield header

        table = Table(show_header=False, header_style="bright_red", border_style="bright_red")

        table.add_column("Identifier", justify="left", style="bold red")

        for player in self:
            table.add_row(player.__rich_console__(console))

        yield table

    def __str__(self, indent=0):
        prefix = " " * indent
        players_str = ""
        for player in self:
            prefix_str = Fore.WHITE + Style.BRIGHT + f"{prefix}│ ┝╍ "
            players_str += prefix_str + f"{player}\n"
        header = Fore.WHITE + Style.BRIGHT + f"{prefix}┌ ALL PLAYERS :\n"
        end = Fore.WHITE + Style.BRIGHT + f"{prefix}└──────────────"
        return header + f"{players_str}" + end

    def __repr__(self):
        return str(self)

    def add_player(self, player: Player) -> None:
        """
        Method that adds a player to the list of players.
        Args:
            player (Player): Player to be added.
        """
        self.data.append(player)

    def player_exists(self, player: Player) -> int:
        """
        Method that checks if a player identifier is already in the list of players.
        Args:
            player (Player): Player to be checked.

        Returns:
            bool: True if the player identifier exists in the list of players.
        """
        if any(p.identifier == player.identifier for p in self.data):
            return 1
        elif (any(p.name.lower() == player.name.lower() for p in self.data) and
              any(p.first_name.lower() == player.first_name.lower() for p in self.data)):
            return 2
        return 3

    def shuffle(self) -> None:
        """
        Method that shuffles the list of players.
        """
        random.shuffle(self.data)

    def convert_to_dict(self) -> dict[str, dict]:
        """
        Method that converts the players' data to a dictionary.
        Returns:
            The dictionary of the players' data.
        """
        return {str(player.identifier): player.convert_to_dict() for player in self}

    def convert_dict_to_players(self, dictionary) -> None:
        """
        Method that converts a players' datas in a dictionary to the Players object.
        Args:
            dictionary (dict): Dictionary to be converted.
        """
        for identifier, attrs in dictionary.items():
            self.add_player(Player(
                attrs["name"],
                attrs["first_name"],
                attrs["birth_date"],
                identifier
            ))

    @staticmethod
    def generate_random_identifier() -> str:
        """
        Method that generates a random identifier. Used only for testing purposes.
        Returns:
            The random identifier.
        """
        alphabet = string.ascii_letters.lower()
        letter_1 = fake.word(ext_word_list=alphabet).capitalize()
        letter_2 = fake.word(ext_word_list=alphabet).capitalize()
        digits = string.digits
        number = ""
        for _ in range(5):
            number += fake.word(ext_word_list=digits)
        return letter_1 + letter_2 + number

    def generate_random_player(self) -> Player:
        """
        Methode that generates a random player identifier. Used only for testing purposes.
        Returns:
            A player object.
        """
        player = Player(fake.last_name(),
                        fake.first_name(),
                        fake.date_of_birth().strftime("%d/%m/%Y"),
                        self.generate_random_identifier())
        return player

    def generate_random_players(self, number_of_players) -> None:
        """
        Method that generates randomly the players list accordingly to the given number of players.
        Used only for testing purposes.
        Args:
            number_of_players (int): Number of players to be generated.
        """
        self.data = [self.generate_random_player() for _ in range(number_of_players)]

    def load_players_from_json(self, file_path) -> bool | None:
        """
        Method that loads the players from a json file.
        Args:
            file_path (Path): Path to the json file.
        Returns (bool) : True if the file was successfully loaded. False otherwise.
        """
        try:
            with open(file_path, encoding="utf-8") as json_file:
                data = json.load(json_file)
                # convert dictionary datas in Player object
                self.convert_dict_to_players(data)
                return True

        except FileNotFoundError:
            console.print(f"[bright_white]{file_path} : [/bright_white][bright_red]❌ file not found ![/bright_red]\n")
            self.save_players_to_json(PLAYERS_DATA_JSON)
            console.print("[bright_green]File Created ![/bright_green]\n")
            return None

    def save_players_to_json(self, file_path) -> bool:
        """
        Method that saves the players to a json file.
        Args:
            file_path (Path): Path to the json file.
        Returns (bool): True if the saved players were saved. False otherwise.
        """
        try:
            file_path.parent.mkdir(exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as json_file:
                players_dict = self.convert_to_dict()
                json.dump(players_dict, json_file, ensure_ascii=False, indent=4)
                return True

        except FileNotFoundError:
            console.print(f"[bright_white]{file_path} : [/bright_white][bright_red]❌ file not found ![/bright_red]\n")
            return False

    def get_player_by_identifier(self, identifier: str) -> Player | None:
        """
        Method that gets a player by identifier.
        Args:
            identifier (str): Identifier of the player to be retrieved.

        Returns:
            The player object with the given identifier. Or None if not found.
        """
        players = [p for p in self if p.identifier == identifier]
        return players[0] if players else None


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
        start = Fore.WHITE + Style.DIM + f"{self.start_date} {self.start_time}" \
            if self.start_date and self.start_time else "Not started"
        end = Fore.WHITE + Style.DIM + f"{self.end_date} {self.end_time}" \
            if self.end_date and self.end_time else "Not finished"

        prefix_dates = Fore.WHITE + Style.DIM + " (from "
        sep = Fore.WHITE + Style.DIM + " → "
        suffix_dates = Fore.WHITE + Style.DIM + ")"
        round_name = Fore.WHITE + Style.BRIGHT + f"{self.round_name}"

        round_str = round_name + prefix_dates + f"{start}" + sep + f"{end}" + suffix_dates

        if not self.matches:
            return f"- The {self.round_name} has no matches yet."

        matches_str = ""
        for match in self.matches:
            matches_str += f"{match}\n"

        prefix = Fore.WHITE + Style.BRIGHT + "- The "
        middle = Fore.WHITE + Style.BRIGHT + " has "
        suffix = Fore.WHITE + Style.BRIGHT + " matches:\n\n"
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

    def specify_random_scores(self) -> None:
        """
        Method that specifies random scores for all matches in the round.
        """
        for match in self.matches:
            scores = self.get_random_scores()
            match.set_scores(scores[0], scores[1])

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
    def __init__(self, name, place, start_date=None, end_date=None, players=None, description="", current_round=1,
                 rounds_number=NUMBER_OF_ROUNDS):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_number = rounds_number
        self.current_round = current_round
        self.rounds = []
        self.description = description

        if players is None:
            self.players = Players()
        elif isinstance(players, Players):
            self.players = players
        else:
            self.players = Players(players)

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
            prefix = Fore.MAGENTA + Style.BRIGHT + "│"
            prefix_rnd = Fore.WHITE + Style.NORMAL + "   │"
            rounds_str = prefix + Fore.WHITE + Style.BRIGHT + "   ┌ ALL ROUNDS :\n"
            for rnd in self.rounds:
                for line in str(rnd).splitlines():
                    rounds_str += prefix + prefix_rnd + f" {line}\n"
            suffix = Fore.WHITE + Style.NORMAL + "   └──────────────\n"
            rounds_str += prefix + suffix

        name = Fore.MAGENTA + Style.BRIGHT + f"{self.name.upper()} "
        place_dates = Fore.WHITE + Style.NORMAL + (f"({self.place}, {self.start_date} → {self.end_date}, "
                                                   f"currently in round {self.current_round} of {self.rounds_number} "
                                                   f"rounds, description : {self.description})\n")
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

    def add_players(self, players: Players) -> None:
        """
        Method that copies the players object and adds them to the tournament Players object.
        Args:
            players (Players): Players object.
        """
        if not isinstance(players, Players):
            players = Players(players)
        for player in players:
            self.players.add_player(player)

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
                print(Fore.YELLOW + "⮞ Scoreboard :")
                for pid, score in sorted(scores.items(), key=lambda kv: kv[1], reverse=True):
                    player = player_by_id.get(pid)
                    label = f"{player.identifier} - {player.name} {player.first_name}" if player else pid
                    print(Fore.YELLOW + f"⮡ {label}: {score}")
                print("\n")

        sorted_players = sorted(self.players, key=lambda p: scores.get(p.identifier, 0.0), reverse=True)
        self.players[:] = sorted_players

    def create_round(self, round_number: int) -> None:
        """
        Method that creates a round object.
        Args:
            round_number (int): The round number.
        """
        if round_number == 1:

            self.players.shuffle()
        else:
            self.sort_players_by_score()

        round_obj = Round(f"Round {round_number}")

        self.create_matches(self.players, round_obj)

        round_obj.set_start_date()

        self.rounds.append(round_obj)

        console.print(round_obj)

    def create_matches(self, players: Players, round_obj: Round) -> None:
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
            "players": self.players.convert_to_dict(),
            "rounds": {rnd.round_name: rnd.convert_to_dict() for rnd in self.rounds}
        }


class Tournaments(UserList):
    def __init__(self, tournaments=None):
        super().__init__(tournaments or [])

    def __rich_console__(self, console, *args, **kwargs):
        title = Panel("[bold turquoise2]ALL TOURNAMENTS[/bold turquoise2]", border_style="bold turquoise2",
                      expand=True)
        yield title
        table = Table(show_header=False, border_style="bold turquoise2")
        table.add_column("Tournament")
        for tournament in self:
            table.add_row(tournament)
        yield table

    def __str__(self):
        tournaments_str = ""
        for tournament in self:
            prefix = Fore.MAGENTA + Style.NORMAL + "├─├─ "
            t = Fore.MAGENTA + Style.NORMAL + f"{tournament}"
            tournaments_str += prefix + t
        title = Fore.MAGENTA + Style.NORMAL + "┌ ALL TOURNAMENTS :\n"
        suffix = Fore.MAGENTA + Style.NORMAL + "└──────────────────"
        return title + f"{tournaments_str}" + suffix

    def __repr__(self):
        return str(self)

    def add_tournament(self, tournament) -> None:
        """
        Method that adds a tournament to the list of tournaments.
        Args:
            tournament (Tournament): Player to be added.
        """
        self.data.append(tournament)

    def tournament_exists(self, tournament) -> bool:
        """
        Method that checks if a tournament name is already in the list of tournaments.
        Args:
            tournament (Tournament): Tournament to be checked.

        Returns:
            bool: True if the tournament name exists in the list of tournaments.
        """
        return any(tournament_obj.name == tournament.name for tournament_obj in self.data)

    def convert_dict_to_tournaments(self, dictionary) -> None:
        """
        Method that converts tournaments' datas in a dictionary to the Tournaments object.
        Args:
            dictionary (dict): Dictionary to be converted.
        """
        for name, attrs in dictionary.items():
            players = Players()
            players_dict = attrs.get("players", {})

            for identifier, player_attrs in players_dict.items():
                player = Player(
                    player_attrs["name"],
                    player_attrs["first_name"],
                    player_attrs["birth_date"],
                    identifier
                )
                players.add_player(player)

            tournament = Tournament(
                name,
                attrs["place"],
                attrs["start_date"],
                attrs["end_date"],
                players,
                attrs.get("description", ""),
                attrs.get("current_round", 1),
                attrs.get("rounds_number", NUMBER_OF_ROUNDS)
            )

            # Rounds
            rounds_dict = attrs.get("rounds", {})
            for rnd_name, rnd_attrs in rounds_dict.items():
                rnd = Round(rnd_name)
                rnd.start_date = rnd_attrs.get("start_date")
                rnd.start_time = rnd_attrs.get("start_time")
                rnd.end_date = rnd_attrs.get("end_date")
                rnd.end_time = rnd_attrs.get("end_time")
                rnd.matches = []

                # rebuild the matches
                matches_dict = rnd_attrs.get("matches", {})
                for _, match_attrs in matches_dict.items():
                    player_1 = players.get_player_by_identifier(match_attrs["player1"]["identifier"])
                    player_2 = players.get_player_by_identifier(match_attrs["player2"]["identifier"])
                    score_1 = match_attrs["player1"]["score"]
                    score_2 = match_attrs["player2"]["score"]
                    color_1 = match_attrs["player1"]["color"]
                    color_2 = match_attrs["player2"]["color"]

                    match = None
                    if player_1 is not None and player_2 is not None:
                        match = Match(player_1, player_2)
                        match.set_scores(player_1, score_1, player_2, score_2)
                        match.set_colors(color_1, color_2)
                    else:
                        print("Un joueur est manquant !")
                    rnd.matches.append(match)

                tournament.rounds.append(rnd)

            self.add_tournament(tournament)

    def load_tournaments_from_json(self, file_path) -> bool:
        """
        Method that loads tournaments from a json file
        Args:
            file_path (Path): Path to the json file to be loaded.

        Returns:
            Returns a boolean indicating if the tournaments were loaded successfully or not.
        """
        try:
            with open(file_path, encoding="utf-8") as json_file:
                data = json.load(json_file)
                # convert dictionary datas in Tournaments object
                self.convert_dict_to_tournaments(data)
                return True

        except FileNotFoundError:
            print(f"{file_path} : ❌ file not found !\n")
            self.save_tournament_to_json(TOURNAMENTS_DATA_JSON)
            print(Fore.GREEN + "File Created !\n")
            return False

    def save_tournament_to_json(self, file_path) -> bool:
        """
        Method that saves tournaments to a json file.
        Args:
            file_path (Path): Path to the json file to be saved.

        Returns:
            Returns a boolean indicating if the tournaments were saved successfully or not.
        """
        try:
            file_path.parent.mkdir(exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as json_file:
                tournaments_dict = self.convert_to_dict()
                json.dump(tournaments_dict, json_file, ensure_ascii=False, indent=4)
                return True

        except FileNotFoundError:
            print(f"{file_path} : ❌ file not found !")
            return False

    def convert_to_dict(self) -> dict[str, dict]:
        """
        Method that converts the tournaments' data to a dictionary.
        Returns:
            The dictionary of the tournaments' data.
        """
        return {tournament.name: tournament.convert_to_dict() for tournament in self}
