import faker
import json
import string
import random
from collections import UserList, defaultdict
from datetime import datetime
from colorama import Fore, init
init(autoreset=True)

NUMBER_OF_ROUNDS = 4
fake = faker.Faker()


class Match:
    def __init__(self, player1, player2, score1=0, score2=0):
        self.match_tuple = ([player1, score1], [player2, score2])

    def __str__(self):
        message = ""
        if self.match_tuple[0][1] == 0:
            message = (f"┌ The match presents :\n"
                       f"┝╍{self.match_tuple[0][0].__str__()}"
                       f"\n│ VS\n"
                       f"┝╍{self.match_tuple[1][0].__str__()}")
        else:
            message = (f"\n┌ The match's results are:\n│\n"
                       f"┝╍{self.match_tuple[0][0].__str__()} - score : {self.match_tuple[0][1]}"
                       f"\n│ VS\n"
                       f"┝╍{self.match_tuple[1][0].__str__()} - score : {self.match_tuple[1][1]}")

        return message

    def __repr__(self):
        return str(self.match_tuple)

    def set_scores(self, score1, score2):
        """
        Method that sets the scores of the match for each player.
        Args:
            score1 (int): Player 1 score.
            score2 (int): Player 2 score.
        """
        self.match_tuple[0][1] = score1
        self.match_tuple[1][1] = score2


class Player:
    def __init__(self, name, first_name, birth_date, identifier):
        self.name = name
        self.first_name = first_name
        self.birth_date = birth_date
        self.identifier = identifier

    def __str__(self):
        return f"{self.identifier} - {self.name.upper()} {self.first_name} born on {self.birth_date}"

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

    def __str__(self):
        players_str = ""
        for player in self:
            players_str += f"┝╍ {player}\n"
        return (f"┌ All players :\n│\n"
                f"{players_str}")

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

    """ def create_static_players(self):
        player1 = Player("Marie", "Nicolas", "28/07/1979", "AH13765")
        player2 = Player("Esneult", "Samuel", "01/05/1979", "CT54896")
        player3 = Player("Dupont", "Jean", "24/05/1987", "BL17953")
        player4 = Player("Testut", "Sylvie", "05/03/1976", "LM47852")
        self.add_player(player1)
        self.add_player(player2)
        self.add_player(player3)
        self.add_player(player4)"""

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
            file_path (str): Path to the json file.
        """
        try:
            with open(file_path, encoding="utf-8") as json_file:
                data = json.load(json_file)

                # convert dictionary datas in Player object
                self.convert_dict_to_players(data)

        except FileNotFoundError:
            print(f"{file_path} : ❌ file not found !")

    def save_players_to_json(self, file_path):
        """
        Method that saves the players to a json file.
        Args:
            file_path (str): Path to the json file.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as json_file:
                players_dict = self.convert_to_dict()
                json.dump(players_dict, json_file, ensure_ascii=False, indent=4)

        except FileNotFoundError:
            print(f"{file_path} : ❌ file not found !")


class Round:
    def __init__(self, round_name):
        self.round_name = round_name
        self.matches = []
        self.start_date = None
        self.start_time = None
        self.end_date = None
        self.end_time = None

    def __str__(self):
        matches_str = ""
        for match in self.matches:
            matches_str += match.__str__() + "\n"

        message = f"The round {self.round_name} has {len(self.matches)} matches :\n"\
                  f"{matches_str}"

        return message

    def __repr__(self):
        return str(self)

    def create_matches(self, players):
        """
        Method that creates a list of matches for a round.
        Args:
            players (Players): Players object.
        """
        i = 0
        while i < len(players):
            p1 = players[i]
            p2 = players[i + 1]
            match = Match(p1, p2)
            self.matches.append(match)
            i += 2

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


class Tournament:
    def __init__(self, name, place, start_date, end_date, description="", current_round=1,
                 rounds_number=NUMBER_OF_ROUNDS):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.rounds_number = rounds_number
        self.current_round = current_round
        self.rounds = []
        self.players = Players()
        self.description = description

    def __str__(self):
        return (f"The tournament {self.name.upper()} in {self.place} started on {self.start_date} "
                f"and ends on {self.end_date} "
                f"is actually in round {self.current_round} of {self.rounds_number} rounds with\n"
                f"{self.players.__str__()} "
                f"\n┕ and with director's description : {self.description}.")

    def __repr__(self):
        return str(self)

    def add_player(self, player):
        """
        Methode that adds a player to the tournament Players object.
        Args:
            player (Player): Player object.
        """
        self.players.append(player)

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
