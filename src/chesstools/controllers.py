from pathlib import Path

from colorama import Fore, init
from jinja2 import Environment, FileSystemLoader

from .models import Player, Players, Tournament, Tournaments
from .views import MainView, PlayerView, ReportView, TournamentView

init(autoreset=True)


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
        # views
        self.view = MainView()

        self.env = Environment(loader=FileSystemLoader('.'))

        # load all templates
        self.templates = {
            "players": self.env.get_template(ALPHABETICALLY_PLAYERS_TEMPLATE_HTML),
            "all_tournaments": self.env.get_template(TOURNAMENTS_TEMPLATE_HTML),
            "current_tournament_players": self.env.get_template(CURRENT_TOURNAMENT_PLAYERS_TEMPLATE_HTML),
            "tournament_rounds_and_matches": self.env.get_template(CURRENT_TOURNAMENT_ROUNDS_MATCHES_TEMPLATE_HTML)
        }

        # Controllers
        self.player_controller = PlayerController()
        self.tournament_controller = TournamentController(self)
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


class TournamentController:
    def __init__(self, main_controller):
        # models
        self.current_tournament = None
        self.tournaments = Tournaments()
        self.main_controller = main_controller

        # View
        self.view = TournamentView()

    def tournaments_menu(self):
        """
        Method that displays the "tournaments" menu.
        """
        while True:
            self.view.display_tournaments_submenu()
            menu = self.view.prompt_for_tournaments_submenu()

            # Dispatching table
            actions = {
                1: self.create_tournament_init,
                2: self.display_update_tournament_sub_menu,
                3: self.display_a_tournament,
                4: self.display_tournaments,
                5: None
            }

            action = actions.get(menu)

            if action is None:
                break

            action()

    def get_tournament(self, tournament_name):
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

    @staticmethod
    def get_all_tournaments():
        """
        Method that gets tournaments object from the json file
        Returns:
            Tournaments object.
        """
        print(Fore.YELLOW + "⮞ Getting tournaments...\n")
        tournaments = Tournaments()

        # loads tournaments datas from json
        tournaments.load_tournaments_from_json(TOURNAMENTS_DATA_JSON)
        return tournaments

    def display_tournaments(self):
        """
        Method that displays tournaments object.
        """
        tournaments = self.get_all_tournaments()
        print(tournaments)

    def display_a_tournament(self):
        """
        Method that displays a tournament.
        """
        self.tournaments = self.get_all_tournaments()
        name = self.view.prompt_for_selecting_tournament(self.tournaments)
        if name.lower() == "q":
            return

        self.current_tournament = self.get_tournament(name)

        print(self.current_tournament)

        if self.current_tournament.is_completed():
            # Tournament completed
            self.display_completed_tournament()

    def create_tournament_init(self):
        """
        Method that launch the creation of a new tournament and checks if enough players.
        Returns:

        """
        players = self.main_controller.player_controller.get_players()
        if len(players) >= 4:
            self.create_tournament()
        elif len(players) in [1, 2, 3]:
            self.main_controller.player_controller.view.display_enough_players()
            return
        else:
            self.main_controller.player_controller.view.display_no_players()
            return

    def create_tournament(self):
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

        self.current_tournament = Tournament(name,
                                             place,
                                             start_date,
                                             end_date,
                                             players=Players(),
                                             description=description)

        players_to_play = self.select_tournament_players(players_number)

        self.current_tournament.add_players(players_to_play)

        # Create round
        self.current_tournament.create_round(self.current_tournament.current_round)

        # Saving to json
        if self.tournaments.tournament_exists(self.current_tournament):
            self.view.display_tournament_exists()
        else:
            self.tournaments.add_tournament(self.current_tournament)
            if self.tournaments.save_tournament_to_json(TOURNAMENTS_DATA_JSON):
                self.view.display_tournament_added(self.current_tournament)

    def display_completed_tournament(self):
        """
        Method that displays a completed tournament object and the winner of the tournament.
        """

        scores, id_to_player = Tournament.compute_player_scores(self.current_tournament)
        if not scores:
            print("No players/scores found.")
            return

        # find max score
        max_score = max(scores.values())

        # filter the players with this score
        winner_ids = [player_id for player_id, score in scores.items() if score == max_score]
        winners = [id_to_player[player_id] for player_id in winner_ids]

        self.view.display_winners(winners, max_score, self.current_tournament.name)

    def tournament_exists(self, tournament_name):
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

    def save_tournament(self, tournament_name):
        """
        Method that saves a tournament.
        Args:
            tournament_name (str): Tournament name.
        """
        for tournament in self.tournaments:
            if tournament.name == tournament_name:
                self.tournaments.remove(tournament)
                self.tournaments.add_tournament(self.current_tournament)

        if self.tournaments.save_tournament_to_json(TOURNAMENTS_DATA_JSON):
            self.view.display_tournament_updated(self.current_tournament)

    def update_tournament(self):
        """
        Method that updates a tournament. Called when the user select the second option in the main menu.
        """

        self.tournaments = self.get_all_tournaments()
        running_tournaments = Tournaments()
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

                if tournament.is_completed():
                    self.current_tournament = tournament
                    self.display_completed_tournament()
                    self.view.display_tournament_completed()
                    continue
                break

            for tournament in self.tournaments:
                if tournament.name == tournament_name:
                    self.current_tournament = tournament
            self.view.display_selected_tournament(tournament_name)

            if self.current_tournament.current_round < 4:
                self.set_tournament_scores()

                self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

                self.current_tournament.current_round += 1

                self.current_tournament.create_round(self.current_tournament.current_round)

                self.save_tournament(tournament_name)

            else:
                self.set_tournament_scores()

                self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

                self.save_tournament(tournament_name)

                self.display_completed_tournament()

    @staticmethod
    def increment_score(player_score, increment):
        player_score += increment

    def set_tournament_scores(self):
        """
        Method that sets the tournament scores.
        """
        tournament = self.current_tournament
        rnd = tournament.rounds[tournament.current_round - 1]
        print(rnd)
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

            match.set_scores(player_1, score_1, player_2, score_2)

        self.view.display_tournament_round_score_saved(rnd.round_name)

    def select_tournament_players(self, players_number):
        """
        Method that selects the tournaments players from all the players in database.
        Args:
            players_number (int): Number of players to select.

        Returns:
            Players object.
        """
        number = int(players_number)
        current_number = 0
        all_players = self.main_controller.player_controller.get_players()
        selected_players = Players()

        while current_number < number:
            players_left = number - current_number
            player_identifier = (self.main_controller.player_controller.view.
                                 prompt_for_selecting_players(all_players, players_left, selected_players))
            player = all_players.get_player_by_identifier(player_identifier)

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

    def display_update_tournament_sub_menu(self):
        """
        Method that displays the "update a tournament" sub menu.
        """
        while True:
            self.view.display_update_tournament_menu()
            submenu = self.view.prompt_for_updating_tournament_menu()

            # Dispatching table
            actions = {
                1: self.display_tournaments,
                2: self.update_tournament,
                3: None
            }

            action = actions.get(submenu)

            if action is None:
                break

            action()


class PlayerController:
    def __init__(self):
        self.view = PlayerView()

    def players_menu(self):
        """
        Method that displays the "players" menu.
        """
        while True:
            self.view.display_players_submenu()
            menu = self.view.prompt_for_players_submenu()

            # Dispatching table
            actions = {
                1: self.add_player_in_database,
                2: self.display_players,
                3: None
            }

            action = actions.get(menu)

            if action is None:
                break

            action()

    @staticmethod
    def get_players():
        """
        Method that gets players object from the json file
        Returns:
            Players object.
        """
        print(Fore.YELLOW + "⮞ Getting players...\n")
        players = Players()

        # loads players datas from json
        players.load_players_from_json(PLAYERS_DATA_JSON)
        return players

    def display_players(self):
        """
        Method that displays players object.
        """
        players = self.get_players()
        print(players)

    def add_player_in_database(self):
        """
        Method that loads the players from the json file, creates a new player object with the datas given
        by the user. The new player datas are also saved in the json file.
        """
        name = self.view.prompt_for_player_name()
        if name.lower() == "q":
            return

        first_name = self.view.prompt_for_player_first_name()
        birth_date = self.view.prompt_for_player_birth_date()
        identifier = self.view.prompt_for_player_identifier()
        player = Player(name, first_name, birth_date, identifier)
        players = self.get_players()

        if players.player_exists(player):
            self.view.display_player_exists()
        else:
            players.add_player(player)
            if players.save_players_to_json(PLAYERS_DATA_JSON):
                self.view.display_player_added(player)


class ReportController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.view = ReportView()

    def reports_menu(self):
        """
        Method that displays the "reports" menu.
        """
        while True:
            self.view.display_reports_menu()
            submenu = self.view.prompt_for_reports_menu()

            # Dispatching table
            actions = {
                1: lambda: self.display_report(report=1),
                2: lambda: self.display_report(report=2),
                3: lambda: self.display_report(report=3),
                4: lambda: self.display_report(report=4),
                5: None
            }

            action = actions.get(int(submenu))

            if action is None:
                break

            action()

    def save_report(self, path, content):
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

    def display_report(self, report):
        """
        Method that displays the report according to the report number given.
        Args:
            report (int): Number of the report in the dispatch table.

        Returns:
            A tuple with the template path and the HTML content.
        """
        def report_alphabetically_players():
            content = self.generate_report_alphabetically_players()
            return ALPHABETICALLY_PLAYERS_REPORT, content

        def report_tournaments():
            content = self.generate_report_tournaments()
            return ALL_TOURNAMENTS_REPORT, content

        def report_current_tournament_players():
            tournaments = self.main_controller.tournament_controller.get_all_tournaments()

            tournament_name = (self.main_controller.tournament_controller.
                               prompt_for_selecting_tournament(tournaments))
            print(tournament_name)
            current_tournament = Tournament("", "")

            for tournament in tournaments:
                if tournament.name == tournament_name:
                    current_tournament = tournament

            content = self.generate_report_current_tournament_players(current_tournament)

            return CURRENT_TOURNAMENT_PLAYERS_REPORT, content

        def report_current_tournament_rounds_and_matches():
            tournaments = self.main_controller.tournament_controller.get_all_tournaments()

            tournament_name = (self.main_controller.tournament_controller.view.
                               prompt_for_selecting_tournament(tournaments))
            print(tournament_name)
            current_tournament = Tournament("", "")

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

    def generate_report_alphabetically_players(self):
        """
        Method that generates the report with the players alphabetically sorted.
        Returns:
            HTML content of the report.
        """
        template = self.main_controller.templates["players"]

        players = self.main_controller.player_controller.get_players()

        sorted_players = sorted(players, key=lambda p: p.name)

        self.view.display_sorted_players(len(sorted_players), Players(sorted_players))

        html = template.render(players=sorted_players)

        return html

    def generate_report_tournaments(self):
        """
        Method that generates the report with the tournaments sorted.
        Returns:
            HTML content of the report.
        """
        tournaments = self.main_controller.tournament_controller.get_all_tournaments()

        sorted_tournaments = sorted(tournaments, key=lambda t: t.name)

        template = template = self.main_controller.templates["all_tournaments"]

        self.view.display_sorted_tournaments(Tournaments(sorted_tournaments))

        html = template.render(tournaments=sorted_tournaments)

        return html

    def generate_report_current_tournament_players(self, tournament):
        """
        Method that generates the report with the current tournament players sorted.
        Args:
            tournament (Tournament): Tournament object.

        Returns:
            HTML content of the report.
        """
        template = self.main_controller.templates["current_tournament"]

        self.view.display_selected_tournament_title(tournament.name)
        for player in tournament.players:
            self.view.display_player(player)

        sorted_players = sorted(tournament.players, key=lambda p: p.name)
        tournament.players = sorted_players

        html = template.render(tournament=tournament)

        return html

    def generate_report_current_tournament_all_rounds_and_matches(self, tournament):
        """
        Method that generates the report with all rounds and matches of the given tournament.
        Args:
            tournament (Tournament): Tournament object.

        Returns:
            HTML content of the report.
        """
        template = self.main_controller.templates["tournament_all_rounds_and_matches"]

        # Display
        self.view.display_selected_tournament_title(tournament.name)
        for rnd in tournament.rounds:
            self.view.display_rnd(rnd)

        # Generate HTML report content
        html = template.render(tournament=tournament)

        return html
