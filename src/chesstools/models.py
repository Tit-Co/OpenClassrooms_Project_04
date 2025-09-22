import faker
import json
import random
import string
from collections import defaultdict, UserList
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)


fake = faker.Faker()
NUMBER_OF_ROUNDS = 4
TOURNAMENT_FOLDER = Path("./data/tournaments/")
TOURNAMENTS_DATA_JSON = TOURNAMENT_FOLDER / Path("./tournaments.json")
PLAYERS_DATA_JSON = TOURNAMENT_FOLDER / Path("./players.json")


class Match:
    def __init__(self, player1, player2, score1=0, score2=0):
        if random.choice([True, False]):
            self.match_tuple = ([player1, score1, "⚪"], [player2, score2, "⚫"])
        else:
            self.match_tuple = ([player2, score2, "⚪"], [player1, score1, "⚫"])

    def __iter__(self):
        return iter(self.match_tuple)

    def __str__(self):
        p1, s1, c1 = self.match_tuple[0]
        p2, s2, c2 = self.match_tuple[1]

        s1_display = s1 if s1 is not None else 0
        s2_display = s2 if s2 is not None else 0

        prefix = Fore.WHITE + Style.BRIGHT + "┝╍ "
        color1 = Fore.WHITE + f"{c1.upper()}"
        color2 = Fore.WHITE + f"{c2.upper()}"
        sep = " - "
        score = " - score: "
        line1 = prefix + f"{p1}" + sep + color1 + score + f"{s1_display}\n"
        bar = "│ "
        vs = Fore.YELLOW + Style.DIM + "VS\n"
        line2 = prefix + f"{p2}" + sep + color2 + score + f"{s2_display}\n"
        return line1 + bar + vs + line2

    def __repr__(self):
        return str(self.match_tuple)

    def set_scores(self, p1, score1, p2, score2):
        """
        Method that sets the scores of the match.
        Args:
            p1 (player): The player 1 associated to score 1.
            score1 (float): The score 1.
            p2 (player): The player 2 associated to score 2.
            score2 (float): The score 2.
        """
        if self.match_tuple[0][0] == p1:
            self.match_tuple[0][1] = score1
            self.match_tuple[1][1] = score2
        elif self.match_tuple[0][0] == p2:

            self.match_tuple[0][1] = score2
            self.match_tuple[1][1] = score1
        else:
            print("Scores bug !")

    def set_colors(self, color1, color2):
        """
        Method that sets the players color in the match.
        Args:
            color1 (float): The color 1.
            color2 (float): The color 2.
        """
        self.match_tuple[0][2] = color1
        self.match_tuple[1][2] = color2

    def convert_to_dict(self):
        p1, s1, c1 = self.match_tuple[0]
        p2, s2, c2 = self.match_tuple[1]
        return {
            "player1": {
                "identifier": p1.identifier,
                "score": s1,
                "color": c1,
            },
            "player2": {
                "identifier": p2.identifier,
                "score": s2,
                "color": c2,
            }
        }


class Player:
    def __init__(self, name, first_name, birth_date, identifier):
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.identifier = identifier

    def __str__(self):
        str_id = Fore.RED + Style.DIM + f"{self.identifier}"
        sep = Fore.WHITE + Style.NORMAL + " - "
        str_na = Fore.BLUE + Style.BRIGHT + f"{self.first_name} {self.name.upper()} "
        str_da = Fore.WHITE + Style.NORMAL + f"born on {self.birth_date}"
        return str_id + sep + str_na + str_da

    def __repr__(self):
        return str(self)

    def convert_to_dict(self):
        """
        Method that converts the player's data to a dictionary.
        Returns: The dictionary of the player's data.
        """
        return {"name": self.name,
                "first_name": self.first_name,
                "birth_date": self.birth_date}


class Players(UserList):
    def __init__(self, players=None):
        super().__init__(players or [])

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

    def add_player(self, player):
        """
        Method that adds a player to the list of players.
        Args:
            player (Player): Player to be added.
        """
        self.data.append(player)

    def player_exists(self, player):
        """
        Method that checks if a player identifier is already in the list of players.
        Args:
            player (Player): Player to be checked.

        Returns:
            bool: True if the player identifier exists in the list of players.
        """
        return any(p.identifier == player.identifier for p in self.data)

    def shuffle(self):
        """
        Method that shuffles the list of players.
        """
        random.shuffle(self.data)

    def convert_to_dict(self):
        """
        Method that converts the players' data to a dictionary.
        Returns:
            The dictionary of the players' data.
        """
        return {str(player.identifier): player.convert_to_dict() for player in self}

    def convert_dict_to_players(self, dictionary):
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
    def generate_random_identifier():
        """
        Method that generates a random identifier. Used only for testing purposes.
        Returns:
            The random identifier.
        """
        alphabet = string.ascii_letters.lower()
        letter1 = fake.word(ext_word_list=alphabet).capitalize()
        letter2 = fake.word(ext_word_list=alphabet).capitalize()
        digits = string.digits
        number = ""
        for _ in range(5):
            number += fake.word(ext_word_list=digits)
        return letter1 + letter2 + number

    def generate_random_player(self):
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

    def generate_random_players(self, number_of_players):
        """
        Method that generates randomly the players list accordingly to the given number of players.
        Used only for testing purposes.
        Args:
            number_of_players (int): Number of players to be generated.
        """
        self.data = [self.generate_random_player() for _ in range(number_of_players)]

    def load_players_from_json(self, file_path):
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
            print(f"{file_path} : ❌ file not found !\n")
            while True:
                answer = input(Fore.YELLOW + "Do you want to create the file ? (y/n)\n")
                if answer in ["Y", "y"]:
                    if self.save_players_to_json(PLAYERS_DATA_JSON):
                        print(Fore.GREEN + "File Created !\n")
                    return True
                elif answer in ["N", "n"]:
                    return False
                else:
                    print(Fore.RED + "You did not enter y or n.\n")
                    continue
            return False

    def save_players_to_json(self, file_path):
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
            print(f"{file_path} : ❌ file not found !")
            return False

    def get_player_by_identifier(self, identifier: str):
        """
        Method that gets a player by identifier.
        Args:
            identifier (str): Identifier of the player to be retrieved.

        Returns:
            The player object with the given identifier. Or None if not found.
        """
        return next((p for p in self if p.identifier == identifier), None)


class Round:
    def __init__(self, round_name):
        self.round_name = round_name
        self.matches = []
        self.start_date = None
        self.start_time = None
        self.end_date = None
        self.end_time = None

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
            return f"The {self.round_name} has no matches yet."

        matches_str = ""
        for match in self.matches:
            matches_str += f"{match}\n"

        prefix = Fore.WHITE + Style.BRIGHT + "The "
        middle = Fore.WHITE + Style.BRIGHT + " has "
        suffix = Fore.WHITE + Style.BRIGHT + " matches:\n\n"
        return prefix + f"{round_str}" + middle + f"{len(self.matches)}" + suffix + f"{matches_str}"

    def __repr__(self):
        return str(self)

    def set_start_date(self):
        """
        Method that sets the start date of the round.
        """
        now = datetime.now()
        self.start_date = now.strftime("%d/%m/%Y")
        self.start_time = now.strftime("%H:%M:%S")

    def set_end_date(self):
        """
        Method that sets the end date of the round.
        """
        now = datetime.now()
        self.end_date = now.strftime("%d/%m/%Y")
        self.end_time = now.strftime("%H:%M:%S")

    @staticmethod
    def get_random_scores():
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

    def specify_random_scores(self):
        """
        Method that specifies random scores for all matches in the round.
        """
        for match in self.matches:
            scores = self.get_random_scores()
            match.set_scores(scores[0], scores[1])

    def convert_to_dict(self):
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

    def is_completed(self):
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

    def add_players(self, players):
        """
        Method that copies the players object and adds them to the tournament Players object.
        Args:
            players (Players): Players object.
        """
        if not isinstance(players, Players):
            players = Players(players)
        for p in players:
            self.players.add_player(p)

    def add_round(self, tournament_round):
        """
        Method that adds a round to the tournament Rounds object.
        Args:
            tournament_round (Round): Round object.
        """
        self.rounds.append(tournament_round)

    @staticmethod
    def compute_player_scores(tournament):
        """
        Method that computes the player scores for all players in the tournament.
        Args:
            tournament (Tournament): Tournament object.

        Returns:
            A score associated to player's id.
        """
        id_to_player = {p.identifier: p for p in tournament.players}
        # init scores to 0.0
        scores = {pid: 0.0 for pid in id_to_player.keys()}

        for rnd in getattr(tournament, "rounds", []):
            for match in getattr(rnd, "matches", []) or []:
                # match.match_tuple = ([Player, score, color], [Player, score, color])
                p1_obj, s1, _ = match.match_tuple[0]
                p2_obj, s2, _ = match.match_tuple[1]

                # convert in float if necessary
                s1_val = float(s1) if s1 is not None else 0.0
                s2_val = float(s2) if s2 is not None else 0.0

                scores[p1_obj.identifier] = scores.get(p1_obj.identifier, 0.0) + s1_val
                scores[p2_obj.identifier] = scores.get(p2_obj.identifier, 0.0) + s2_val

        return scores, id_to_player

    def sort_players_by_score(self, verbose=False):
        """
        Method that sorts the players in Players object by their scores.
        Args:
            verbose (bool): Boolean flag to determine if scoreboard should be printed.
        """
        scores = defaultdict(float)

        print(Fore.YELLOW + "⮞ Sorting players by score ...")

        player_by_id = {p.identifier: p for p in self.players}

        for rnd in (self.rounds or []):
            for match in rnd.matches:

                pairs = match.match_tuple

                for pair in pairs:
                    player_entry = pair[0]
                    raw_score = pair[1]
                    pid = player_entry.identifier
                    sc = float(raw_score)
                    scores[pid] += sc

            for p in self.players:
                scores.setdefault(p.identifier, 0.0)

            # debug : display the scoreboard if asked
            if verbose:
                print(Fore.YELLOW + "⮞ Scoreboard :")
                for pid, sc in sorted(scores.items(), key=lambda kv: kv[1], reverse=True):
                    pl = player_by_id.get(pid)
                    label = f"{pl.identifier} - {pl.name} {pl.first_name}" if pl else pid
                    print(Fore.YELLOW + f"⮡ {label}: {sc}")
                print("\n")

        sorted_players = sorted(self.players, key=lambda p: scores.get(p.identifier, 0.0), reverse=True)
        self.players[:] = sorted_players

    def create_round(self, round_number):
        """
        Method that creates a round object.
        Args:
            round_number (int): The round number.
        """
        if round_number == 1:
            # shuffles players
            self.players.shuffle()
        else:
            self.sort_players_by_score()

        # create round
        round_obj = Round(f"Round {round_number}")

        # create matches
        self.create_matches(self.players, round_obj)

        # Set start date/time
        round_obj.set_start_date()

        # Append round to tournament
        self.rounds.append(round_obj)

        print(round_obj)

    def create_matches(self, players, round_obj):
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

    def match_already_played(self, player1, player2):
        """
        Method that checks if two players have already faced each other in this tournament.
        Args:
            player1 (Player): Player 1 object.
            player2 (Player): Player 2 object.

        Returns:
            A boolean indicating if the player 1 has already played with player 2.
        """
        pair_to_check = frozenset([player1.identifier, player2.identifier])

        for rnd in self.rounds:
            for match in rnd.matches:
                p1 = match.match_tuple[0][0].identifier
                p2 = match.match_tuple[1][0].identifier
                existing_pair = frozenset([p1, p2])

                if pair_to_check == existing_pair:
                    return True
        return False

    def convert_to_dict(self):
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

    def add_tournament(self, tournament):
        """
        Method that adds a tournament to the list of tournaments.
        Args:
            tournament (Tournament): Player to be added.
        """
        self.data.append(tournament)

    def tournament_exists(self, tournament):
        """
        Method that checks if a tournament name is already in the list of tournaments.
        Args:
            tournament (Tournament): Tournament to be checked.

        Returns:
            bool: True if the tournament name exists in the list of tournaments.
        """
        return any(t.name == tournament.name for t in self.data)

    def convert_dict_to_tournaments(self, dictionary):
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
                    p1 = players.get_player_by_identifier(match_attrs["player1"]["identifier"])
                    p2 = players.get_player_by_identifier(match_attrs["player2"]["identifier"])
                    s1 = match_attrs["player1"]["score"]
                    s2 = match_attrs["player2"]["score"]
                    c1 = match_attrs["player1"]["color"]
                    c2 = match_attrs["player2"]["color"]

                    match = Match(p1, p2)
                    match.set_scores(p1, s1, p2, s2)
                    match.set_colors(c1, c2)
                    rnd.matches.append(match)

                tournament.rounds.append(rnd)

            self.add_tournament(tournament)

    def load_tournaments_from_json(self, file_path):
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
            while True:
                answer = input("Do you want to create the file ? (y/n)\n")
                if answer in ["Y", "y"]:
                    if self.save_tournament_to_json(TOURNAMENTS_DATA_JSON):
                        print(Fore.GREEN + "File Created !\n")
                    return True
                elif answer in ["N", "n"]:
                    return False
                else:
                    print(Fore.RED + "You did not enter y or n.\n")
                    continue
            return False

    def save_tournament_to_json(self, file_path):
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

    def convert_to_dict(self):
        """
        Method that converts the tournaments' data to a dictionary.
        Returns:
            The dictionary of the tournaments' data.
        """
        return {tournament.name: tournament.convert_to_dict() for tournament in self}
