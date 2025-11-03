from __future__ import annotations

# Standard library imports
import json
import random
import sys
from collections import UserList
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from rich.console import Console

from .models import Match, Player, Round, Tournament
from .views import MainView, PlayerView, ReportView, TournamentView

console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",
    width=200
)

NUMBER_OF_ROUNDS = 4

# Base paths
TOURNAMENT_FOLDER = Path("./data/tournaments/")
REPORTS_FOLDER = Path("./data/reports/")

# Json
TOURNAMENTS_DATA_JSON = TOURNAMENT_FOLDER / Path("./tournaments.json")
PLAYERS_DATA_JSON = TOURNAMENT_FOLDER / Path("./players.json")

# Reports paths
ALPHABETICALLY_PLAYERS_REPORT = REPORTS_FOLDER / Path("./1_report_alphabetically_players.html")
ALL_TOURNAMENTS_REPORT = REPORTS_FOLDER / Path("./2_report_all_tournaments.html")
CURRENT_TOURNAMENT_PLAYERS_REPORT = REPORTS_FOLDER / Path("./3_report_current_tournament_players.html")
CURRENT_TOURNAMENT_ROUNDS_AND_MATCHES_REPORT = (REPORTS_FOLDER
                                                / Path("./4_report_current_tournament_rounds_matches.html"))

# Templates paths
ALPHABETICALLY_PLAYERS_TEMPLATE_HTML = "./src/templates/report_alphabetically_players_template.html"
TOURNAMENTS_TEMPLATE_HTML = "./src/templates/report_tournaments_template.html"
CURRENT_TOURNAMENT_PLAYERS_TEMPLATE_HTML = "./src/templates/report_current_tournament_players_template.html"
CURRENT_TOURNAMENT_ROUNDS_MATCHES_TEMPLATE_HTML = ("./src/templates/report_current_tournament_"
                                                   "rounds_matches_template.html")


class MainController:
    def __init__(self):
        self.view = MainView()

        self.env = Environment(loader=FileSystemLoader('.'))

        self.templates = {
            "players": self.env.get_template(ALPHABETICALLY_PLAYERS_TEMPLATE_HTML),
            "all_tournaments": self.env.get_template(TOURNAMENTS_TEMPLATE_HTML),
            "current_tournament_players": self.env.get_template(CURRENT_TOURNAMENT_PLAYERS_TEMPLATE_HTML),
            "tournament_rounds_and_matches": self.env.get_template(CURRENT_TOURNAMENT_ROUNDS_MATCHES_TEMPLATE_HTML)
        }
        self.tournament_controller = TournamentController(self)
        self.player_controller = PlayerController(self)
        self.report_controller = ReportController(self)

    def run(self):
        """
        Method that runs the main controller.
        """
        while True:
            self.view.display_main_menu()
            menu = self.view.prompt_for_main_menu()

            # Dispatching table
            actions = {
                1: self.tournament_controller.tournaments_menu,
                2: self.player_controller.players_menu,
                3: self.report_controller.reports_menu,
                4: self.goodbye
            }

            action = actions.get(menu)
            action()

    def goodbye(self):
        """
        Method that close the application.
        """
        self.view.display_goodbye()
        exit(1)


class TournamentsManager(UserList):
    def __init__(self, tournaments=None):
        super().__init__(tournaments or [])

    def add_tournament(self, tournament: Tournament) -> None:
        """
        Method that adds a tournament to the list of tournaments.
        Args:
            tournament (Tournament): Player to be added.
        """
        self.data.append(tournament)

    def tournament_exists(self, tournament: Tournament) -> bool:
        """
        Method that checks if a tournament name is already in the list of tournaments.
        Args:
            tournament (Tournament): Tournament to be checked.

        Returns:
            bool: True if the tournament name exists in the list of tournaments.
        """
        return any(tournament_obj.name == tournament.name for tournament_obj in self.data)

    def convert_dict_to_tournaments(self, controller: TournamentController, dictionary: dict) -> None:
        """
        Method that converts tournaments' datas in a dictionary to the Tournaments object.
        Args:
            controller (TournamentController): Controller object.
            dictionary (dict): Dictionary to be converted.
        """
        for name, attrs in dictionary.items():
            players = PlayersManager()
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
                attrs["rounds_number"],
                attrs["start_date"],
                attrs["end_date"],
                attrs.get("description", ""),
                attrs.get("current_round", 1),
            )
            tournament.add_players(players)

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
                        controller.set_match_scores(match, player_1, score_1, player_2, score_2)
                        match.set_colors(color_1, color_2)
                    else:
                        return
                    rnd.matches.append(match)

                tournament.rounds.append(rnd)

            self.add_tournament(tournament)

    def load_tournaments_from_json(self, controller: TournamentController, file_path: Path) -> bool:
        """
        Method that loads tournaments from a json file
        Args:
            controller (TournamentController): Controller object.
            file_path (Path): Path to the json file to be loaded.

        Returns:
            Returns a boolean indicating if the tournaments were loaded successfully or not.
        """
        try:
            with open(file_path, encoding="utf-8") as json_file:
                data = json.load(json_file)
                # convert dictionary datas in Tournaments object
                self.convert_dict_to_tournaments(controller, data)
                return True

        except FileNotFoundError:
            self.save_tournament_to_json(controller, TOURNAMENTS_DATA_JSON)
            return False

    def save_tournament_to_json(self, controller: TournamentController, file_path: Path) -> bool:
        """
        Method that saves tournaments to a json file.
        Args:
            controller (TournamentController): The TournamentController object.
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
            controller.view.display_file_not_found(file_path)
            return False

    def convert_to_dict(self) -> dict[str, dict]:
        """
        Method that converts the tournaments' data to a dictionary.
        Returns:
            The dictionary of the tournaments' data.
        """
        return {tournament.name: tournament.convert_to_dict() for tournament in self}


class TournamentController:
    def __init__(self, main_controller):
        self.current_tournament = None
        self.tournaments = TournamentsManager()
        self.main_controller = main_controller

        self.view = TournamentView()

    def tournaments_menu(self) -> None:
        """
        Method that displays the "tournaments" menu.
        """
        while True:
            self.view.display_tournaments_submenu()
            menu = self.view.prompt_for_tournaments_submenu()

            if menu == 5:
                break

            # Dispatching table
            actions = {
                1: self.create_tournament_init,
                2: self.display_update_tournament_sub_menu,
                3: self.display_a_tournament,
                4: self.display_tournaments
            }

            action = actions.get(menu)

            action()

    def get_tournament(self, tournament_name: str) -> Tournament | None:
        """
        Method that gets a tournament by name.
        Args:
            tournament_name (str): Tournament name.

        Returns:
            The tournament object. Or None otherwise.
        """
        for t in self.tournaments:
            if t.name == tournament_name:
                return t
        return None

    def get_all_tournaments(self) -> TournamentsManager:
        """
        Method that gets tournaments object from the json file
        Returns:
            Tournaments object.
        """
        tournaments = TournamentsManager()

        tournaments.load_tournaments_from_json(self, TOURNAMENTS_DATA_JSON)
        return tournaments

    def display_a_tournament(self) -> None:
        """
        Method that displays a tournament.
        """
        self.tournaments = self.get_all_tournaments()
        name = self.view.prompt_for_selecting_tournament(self.tournaments)
        if name.lower() == "q":
            return

        self.current_tournament = self.get_tournament(name)

        self.view.display_tournament(self.current_tournament)

        if self.current_tournament.is_completed():
            self.display_completed_tournament()

    def display_tournaments(self) -> None:
        """
        Method that displays all the tournaments.
        """
        tournaments = self.get_all_tournaments()
        self.view.display_tournaments(tournaments)

    def create_tournament_init(self):
        """
        Method that launch the creation of a new tournament and checks if enough players.
        Returns:

        """
        self.main_controller.player_controller.get_players()

        players = self.main_controller.player_controller.players_manager
        if len(players) >= 4:
            self.create_tournament()
        elif len(players) in [1, 2, 3]:
            self.main_controller.player_controller.view.display_enough_players()
            return
        else:
            self.main_controller.player_controller.view.display_no_players()
            return

    def create_round(self, round_number: int) -> Round:
        """
        Method that creates a new round.
        Args:
            round_number (int): Round number.

        Returns:
            The round object.
        """
        ordered = []
        if round_number == 1:
            ordered = list(self.current_tournament.players)
            import random
            random.shuffle(ordered)
        else:
            ordered = self.current_tournament.sort_players_by_score()

        round_obj = self.current_tournament.create_round(round_number, ordered)
        return round_obj

    def create_tournament(self) -> None:
        """
        Method that creates a tournament object.
        """
        while True:
            name = self.view.prompt_for_tournament_name()
            if name.lower() == "q":
                return

            self.tournaments = self.get_all_tournaments()
            if any(t.name == name for t in self.tournaments):
                self.view.display_tournament_name_exists()
                continue
            else:
                break

        place = self.view.prompt_for_tournament_place()
        start_date = self.view.prompt_for_tournament_start_date()
        end_date = self.view.prompt_for_tournament_end_date()
        description = self.view.prompt_for_tournament_description()
        players_number = self.view.prompt_for_tournament_players_number()
        rounds_number = self.view.prompt_for_selecting_tournament_rounds_number()

        self.current_tournament = Tournament(name=name,
                                             place=place,
                                             rounds_number=rounds_number,
                                             start_date=start_date,
                                             end_date=end_date,
                                             description=description)

        players_to_play = self.select_tournament_players(int(players_number))

        self.current_tournament.add_players(players_to_play)

        self.create_round(self.current_tournament.current_round)

        if self.tournaments.tournament_exists(self.current_tournament):
            self.view.display_tournament_exists()
        else:
            self.tournaments.add_tournament(self.current_tournament)
            if self.tournaments.save_tournament_to_json(self, TOURNAMENTS_DATA_JSON):
                self.view.display_tournament_added(self.current_tournament)

    def display_completed_tournament(self) -> None:
        """
        Method that displays a completed tournament object and the winner of the tournament.
        """

        scores, id_to_player = Tournament.compute_player_scores(self.current_tournament)
        if not scores:
            self.view.display_no_scores_found()
            return

        # find max score
        max_score = max(scores.values())

        # filter the players with this score
        winner_ids = [player_id for player_id, score in scores.items() if score == max_score]
        winners = [id_to_player[player_id] for player_id in winner_ids]

        self.view.display_winners(winners, max_score, self.current_tournament.name)

    def tournament_exists(self, tournament_name: str) -> bool:
        """
        Method that checks if a tournament exists.
        Args:
            tournament_name (str): The name of the tournament.

        Returns:
            Boolean: True if the tournament exists. False otherwise.
        """
        for tournament in self.tournaments:
            if tournament.name == tournament_name:
                return True
        return False

    def save_tournament(self, tournament_name: str) -> None:
        """
        Method that saves a tournament.
        Args:
            tournament_name (str): Tournament name.
        """
        for tournament in self.tournaments:
            if tournament.name == tournament_name:
                self.tournaments.remove(tournament)
                self.tournaments.add_tournament(self.current_tournament)

        if self.tournaments.save_tournament_to_json(self, TOURNAMENTS_DATA_JSON):

            self.view.display_tournament_updated(self.current_tournament)

    def set_match_scores(self, match: Match,
                         player_1: Player,
                         score_1: float,
                         player_2: Player,
                         score_2: float) -> None:
        """
        Method that sets the scores of the match.
        Args:
            match (Match): Match object.
            player_1 (Player): The player 1 associated to score 1.
            score_1 (float): The score 1.
            player_2 (Player): The player 2 associated to score 2.
            score_2 (float): The score 2.
        """

        p1, s1, c1 = match.match_tuple[0]
        p2, s2, c2 = match.match_tuple[1]

        if p1 == player_1:
            match.match_tuple = (
                (p1, score_1, c1),
                (p2, score_2, c2),
            )
        elif p1 == player_2:
            match.match_tuple = (
                (p1, score_2, c1),
                (p2, score_1, c2),
            )
        else:
            self.view.display_scores_bug()

    def update_tournament(self) -> None:
        """
        Method that updates a tournament. Called when the user select the second option in the main menu.
        """

        self.tournaments = self.get_all_tournaments()
        running_tournaments = TournamentsManager()
        for tournament in self.tournaments:
            if not tournament.is_completed():
                running_tournaments.add_tournament(tournament)

        if len(running_tournaments) == 0:
            self.view.display_all_tournaments_completed()
        else:

            while True:
                tournament_name = self.view.prompt_for_selecting_tournament(running_tournaments)

                if tournament_name.lower() == "q":
                    return

                tournament = self.get_tournament(tournament_name)

                if tournament is not None and tournament.is_completed():
                    self.current_tournament = tournament
                    self.display_completed_tournament()
                    self.view.display_tournament_completed()
                    continue
                break

            for tournament in self.tournaments:
                if tournament.name == tournament_name:
                    self.current_tournament = tournament
            self.view.display_selected_tournament(tournament_name)

            if self.current_tournament.current_round < int(self.current_tournament.rounds_number):
                self.setting_scores_process(tournament_name)

                answer = self.view.prompt_for_asking_to_continue_tournament_filling()
                if answer:
                    while self.current_tournament.current_round < self.current_tournament.rounds_number:

                        self.setting_scores_process(tournament_name)

            if self.current_tournament.current_round == int(self.current_tournament.rounds_number):
                self.finish_scores_process(tournament_name)

    def finish_scores_process(self, tournament_name: str) -> None:
        """
        Method that finishes scoring process by completes the tournament.
        Args:
            tournament_name (str): the tournament name.
        """
        self.set_tournament_scores()

        self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

        self.save_tournament(tournament_name)

        self.display_completed_tournament()

    def setting_scores_process(self, tournament_name: str) -> None:
        """
        Method that sets the scores of the matches in the current round or the tournament and
        initialize the next round.
        Args:
            tournament_name (str): The name of the tournament.
        """
        self.set_tournament_scores()

        self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

        self.current_tournament.current_round += 1

        self.current_tournament.create_round(self.current_tournament.current_round,
                                             self.current_tournament.sort_players_by_score())

        self.save_tournament(tournament_name)

    @staticmethod
    def increment_score(player_score: float, increment: float) -> None:
        """
        Method that increments a player score.
        Args:
            player_score (float): The player score.
            increment (float): The amount to increment.
        """
        player_score += increment

    def set_tournament_scores(self):
        """
        Method that sets the tournament scores.
        """
        tournament = self.current_tournament
        rnd = tournament.rounds[tournament.current_round - 1]

        self.view.display_setting_scores_title()
        self.view.display_round(rnd)

        for match in rnd.matches:
            player_1, _, _ = match.match_tuple[0]
            player_2, _, _ = match.match_tuple[1]

            score_1 = self.main_controller.player_controller.view.prompt_for_adding_player_score(player_1)

            # Dispatching table
            actions = {
                0: 1.0,
                0.5: 0.5,
                1.0: 0
            }

            score_2 = actions.get(float(score_1), 0)

            self.set_match_scores(match, player_1, score_1, player_2, score_2)

        self.view.display_tournament_round_score_saved(rnd.round_name)

    def select_tournament_players(self, players_number: int) -> PlayersManager:
        """
        Method that selects the tournaments players from all the players in database.
        Args:
            players_number (int): Number of players to select.

        Returns:
            PlayersManager object.
        """
        number = int(players_number)
        current_number = 0

        self.main_controller.player_controller.get_players()

        all_players = self.main_controller.player_controller.players_manager.all_players()
        selected_players = PlayersManager()

        while current_number < number:
            players_left = number - current_number
            player_identifier = (self.main_controller.player_controller.view.
                                 prompt_for_selecting_players(all_players, players_left, selected_players))
            player = self.main_controller.player_controller.players_manager.get_player_by_identifier(player_identifier)

            if player is None:
                self.view.display_player_not_found()
                continue

            if any(p.identifier == player.identifier for p in selected_players):
                self.view.display_player_exists()
                continue

            selected_players.add_player(player)
            current_number += 1
            self.view.display_player_added(player, current_number, number)

        return selected_players

    def display_update_tournament_sub_menu(self) -> None:
        """
        Method that displays the "update a tournament" sub menu.
        """
        while True:
            self.view.display_update_tournament_menu()
            submenu = self.view.prompt_for_updating_tournament_menu()

            if submenu == 3:
                break

            # Dispatching table
            actions = {
                1: self.display_tournaments,
                2: self.update_tournament
            }

            action = actions.get(submenu)

            action()


class PlayersManager(UserList):
    def __init__(self, players=None):
        super().__init__(players or [])

    def all_players(self) -> list["Player"]:
        return list(self.data)

    def add_player(self, player: Player) -> None:
        """
        Method that adds a player to the list of players.
        Args:
            player (Player): Player to be added.
        """
        self.data.append(player)

    def player_names_exist(self, name: str, first_name: str) -> bool:
        """
        Method that checks if a player names already exist.
        Args:
            name (str): The player name.
            first_name (str): The player first name.

        Returns:
            Boolean: True if the player names already exist. False otherwise.
        """
        name, first_name = (name or "").lower(), (first_name or "").lower()
        return any(
            (p.name or "").lower() == name and
            (p.first_name or "").lower() == first_name
            for p in self.data
        )

    def player_identifier_exists(self, identifier: str) -> bool:
        """
        Method that checks if a player identifier already exists.
        Args:
            identifier (str): The player identifier.

        Returns:
            Boolean: True if the player identifier already exists. False otherwise.
        """
        return any(p.identifier == identifier for p in self.data)

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

    def load_players_from_json(self, controller: PlayerController, file_path: Path) -> bool | None:
        """
        Method that loads the players from a json file.
        Args:
            controller (PlayerController): Controller object.
            file_path (Path): Path to the json file.
        Returns (bool) : True if the file was successfully loaded. False otherwise.
        """
        try:
            with open(file_path, encoding="utf-8") as json_file:
                data = json.load(json_file)
                self.convert_dict_to_players(data)
                return True

        except FileNotFoundError:
            self.save_players_to_json(controller, PLAYERS_DATA_JSON)
            return None

    def save_players_to_json(self, controller: PlayerController, file_path: Path) -> bool:
        """
        Method that saves the players to a json file.
        Args:
            controller (PlayerController): The controller object.
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
            controller.view.display_file_not_found(file_path)
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


class PlayerController:
    def __init__(self, main_controller) -> None:
        self.view = PlayerView()
        self.players_manager = PlayersManager()
        self.main_controller = main_controller

    def players_menu(self) -> None:
        """
        Method that displays the "players" menu.
        """
        while True:
            self.view.display_players_submenu()
            menu = self.view.prompt_for_players_submenu()

            if menu == 3:
                break

            # Dispatching table
            actions = {
                1: self.add_player_in_database,
                2: self.display_players
            }

            action = actions.get(menu)

            action()

    def get_players(self) -> None:
        """
        Method that gets players object from the json file
        Returns:
            Players object.
        """
        self.players_manager.clear()
        self.players_manager.load_players_from_json(self, PLAYERS_DATA_JSON)

    def display_players(self) -> None:
        """
        Method that displays players object.
        """
        self.get_players()

        self.view.display_players(self.players_manager)

    def add_player_in_database(self) -> None:
        """
        Method that loads the players from the json file, creates a new player object with the datas given
        by the user. The new player datas are also saved in the json file.
        """
        self.get_players()

        while True:
            name = self.view.prompt_for_player_name()
            if name.lower() == "q":
                return

            first_name = self.view.prompt_for_player_first_name()

            if self.players_manager.player_names_exist(name, first_name):
                self.view.display_player_exists()
                continue
            else:
                break

        birth_date = self.view.prompt_for_player_birth_date()

        while True:
            identifier = self.view.prompt_for_player_identifier()

            if self.players_manager.player_identifier_exists(identifier):
                self.view.display_player_identifier_exists()
                continue
            else:
                break

        player = Player(name.upper(), first_name.capitalize(), birth_date, identifier)

        self.players_manager.add_player(player)

        if self.players_manager.save_players_to_json(self, PLAYERS_DATA_JSON):
            self.view.display_player_added(player)


class ReportController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = ReportView()

    def reports_menu(self) -> None:
        """
        Method that displays the "reports" menu.
        """
        while True:
            self.view.display_reports_menu()
            submenu = self.view.prompt_for_reports_menu()

            if submenu == 5:
                break

            # Dispatching table
            actions = {
                1: lambda: self.display_report(report=1),
                2: lambda: self.display_report(report=2),
                3: lambda: self.display_report(report=3),
                4: lambda: self.display_report(report=4)
            }

            action = actions.get(int(submenu))

            action()

    def save_report(self, path: Path, content: str) -> bool:
        """
        Method that saves the report with the given path.
        Args:
            path (Path): Path to save the report.
            content (str): Content of the report.

        Returns:
            Boolean : True if the report was saved. False otherwise.
        """
        try:
            output_path = Path(path)
            output_path.parent.mkdir(exist_ok=True)
            with open(path, "w", encoding="utf-8") as html_file:
                html_file.write(content)
                return True

        except FileNotFoundError:
            self.view.display_file_not_found(path)
            return False

    def display_report(self, report: int) -> None:
        """
        Method that displays the report according to the report number given.
        Args:
            report (int): Number of the report in the dispatch table.

        Returns:
            A tuple with the template path and the HTML content.
        """
        def report_alphabetically_players() -> tuple[Path, str]:
            """
            Method that returns a tuple containing the report path and the html content of the report for
            alphabetically sorted club players.
            Returns:
                The report path and the html content of the report for alphabetically sorted club players.
            """
            content = self.generate_report_alphabetically_players()
            return ALPHABETICALLY_PLAYERS_REPORT, content

        def report_tournaments() -> tuple[Path, str]:
            """
            Method that returns a tuple containing the report path and the html content of the report for
            all sorted tournaments.
            Returns:
                The report path and the html content of the report of all sorted tournaments.
            """
            content = self.generate_report_tournaments()
            return ALL_TOURNAMENTS_REPORT, content

        def report_current_tournament_players() -> tuple[Path, str]:
            """
            Method that returns a tuple containing the report path and the html content of the report for
            sorted players in the current tournament.
            Returns:
                The report path and the html content of the report for sorted players in the current tournament.
            """
            tournaments = self.main_controller.tournament_controller.get_all_tournaments()

            tournament_name = (self.main_controller.tournament_controller.view.
                               prompt_for_selecting_tournament(tournaments))

            current_tournament = Tournament("", "", 4)

            for tournament in tournaments:
                if tournament.name == tournament_name:
                    current_tournament = tournament

            content = self.generate_report_current_tournament_players(current_tournament)

            return CURRENT_TOURNAMENT_PLAYERS_REPORT, content

        def report_current_tournament_rounds_and_matches() -> tuple[Path, str]:
            """
            Method that returns a tuple containing the report path and the html content of the report for
            all rounds and matches in the current tournament.
            Returns:
                The report path and the html content of the report for all rounds and matches
                in the current tournament.
            """
            tournaments = self.main_controller.tournament_controller.get_all_tournaments()

            tournament_name = (self.main_controller.tournament_controller.view.
                               prompt_for_selecting_tournament(tournaments))

            current_tournament = Tournament("", "", 4)

            for tournament in tournaments:
                if tournament.name == tournament_name:
                    current_tournament = tournament

            content = self.generate_report_current_tournament_all_rounds_and_matches(current_tournament)

            return CURRENT_TOURNAMENT_ROUNDS_AND_MATCHES_REPORT, content

        # --- Dispatch Table ---
        reports = {
            1: report_alphabetically_players,
            2: report_tournaments,
            3: report_current_tournament_players,
            4: report_current_tournament_rounds_and_matches
        }

        while True:
            answer = self.view.prompt_for_generating_report().strip().lower()
            if answer == "y":
                if report not in reports:
                    self.view.display_invalid_report_number()
                    break
                path, content = reports[report]()

                self.save_report(path, content)
                self.view.display_report_generated(path)
                break

            elif answer == "n":
                self.view.display_cancelled()
                break
            else:
                self.view.display_yes_no()

    def generate_report_alphabetically_players(self) -> str:
        """
        Method that generates the report with the players alphabetically sorted.
        Returns:
            HTML content of the report.
        """
        template = self.main_controller.templates["players"]

        self.main_controller.player_controller.get_players()

        players = self.main_controller.player_controller.players_manager

        sorted_players = sorted(players, key=lambda p: p.name)

        self.view.display_sorted_players(len(sorted_players), PlayersManager(sorted_players))

        html = template.render(players=sorted_players)

        return html

    def generate_report_tournaments(self) -> str:
        """
        Method that generates the report with the tournaments sorted.
        Returns:
            HTML content of the report.
        """
        tournaments = self.main_controller.tournament_controller.get_all_tournaments()

        sorted_tournaments = sorted(tournaments, key=lambda t: t.name)

        template = template = self.main_controller.templates["all_tournaments"]

        tournament_view = self.main_controller.tournament_controller.view

        self.view.display_sorted_tournaments(TournamentsManager(sorted_tournaments).data, tournament_view)

        html = template.render(tournaments=sorted_tournaments)

        return html

    def generate_report_current_tournament_players(self, tournament: Tournament) -> str:
        """
        Method that generates the report with the current tournament players sorted.
        Args:
            tournament (Tournament): Tournament object.

        Returns:
            HTML content of the report.
        """
        template = self.main_controller.templates["current_tournament_players"]

        self.view.display_selected_tournament_title(tournament.name)

        sorted_players = sorted(tournament.players, key=lambda p: p.name)

        self.view.display_sorted_players(len(sorted_players), PlayersManager(sorted_players))

        tournament.players = sorted_players

        html = template.render(tournament=tournament)

        return html

    def generate_report_current_tournament_all_rounds_and_matches(self, tournament: Tournament) -> str:
        """
        Method that generates the report with all rounds and matches of the given tournament.
        Args:
            tournament (Tournament): Tournament object.

        Returns:
            HTML content of the report.
        """
        template = self.main_controller.templates["tournament_rounds_and_matches"]

        self.view.display_selected_tournament_title(tournament.name)

        for rnd in tournament.rounds:
            self.view.display_rnd(rnd, self.main_controller.tournament_controller.view)

        html = template.render(tournament=tournament)

        return html
