from .models import Player, Players, Tournament, Tournaments
from .views import View
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from colorama import Fore, Style, init
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


class Controller:
    def __init__(self, the_view):
        # models
        self.current_tournament = None
        self.tournaments = Tournaments()

        # views
        self.view = the_view

    def run(self):
        """
        Method that runs the controller.
        """
        while True:
            self.view.display_main_menu()
            menu = self.view.prompt_for_main_menu()

            match menu:
                case 1:
                    if len(self.get_players()) >= 4:
                        self.create_tournament()
                    elif len(self.get_players()) in [1, 2, 3]:
                        print(Fore.RED + "\nThere is not enough players to create a tournament.\n")
                        continue
                    else:
                        print(Fore.RED + "\nNo players found. "
                                         "You can not create a new tournament before adding new players.\n")
                        continue
                case 2:
                    self.display_tournaments_sub_menu()
                case 3:
                    self.add_player_in_database()
                case 4:
                    self.display_players()
                case 5:
                    self.display_a_tournament()
                case 6:
                    self.display_tournaments()
                case 7:
                    self.display_reports_sub_menu()
                case 8:
                    print(Style.BRIGHT + Fore.RED + "👋 Goodbye ! 👋")
                    break

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
        if players.load_players_from_json(PLAYERS_DATA_JSON):
            return players
        else:
            print(Style.BRIGHT + Fore.RED + "👋 Goodbye ! 👋")
            exit(1)

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
        if tournaments.load_tournaments_from_json(TOURNAMENTS_DATA_JSON):
            return tournaments
        else:
            print(Style.BRIGHT + Fore.RED + "👋 Goodbye ! 👋")
            exit(1)

    def display_players(self):
        """
        Method that displays players object.
        """
        players = self.get_players()
        print(players)

    def display_tournaments(self):
        """
        Method that displays tournaments object.
        """
        tournaments = self.get_all_tournaments()
        print(tournaments)

    def display_a_tournament(self):
        self.tournaments = self.get_all_tournaments()
        name = self.view.prompt_for_selecting_tournament(self.tournaments)
        self.current_tournament = self.get_tournament(name)

        print(self.current_tournament)

        if self.current_tournament.is_completed():
            # Tournament completed
            self.display_completed_tournament()

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
                print("❌ The tournament's name already exists. Please choose another one.\n")
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

        print(self.current_tournament)

        # Saving to json
        if self.tournaments.tournament_exists(self.current_tournament):
            print(Fore.YELLOW + "❌ Tournament already in the database !\n")
        else:
            self.tournaments.add_tournament(self.current_tournament)
            if self.tournaments.save_tournament_to_json(TOURNAMENTS_DATA_JSON):
                print(Fore.YELLOW + f"✅ New tournament added to database !\n{self.current_tournament}")

    def display_completed_tournament(self):
        """
        Method that displays a completed tournament object and th winner of the tournament.
        """
        # Tournament completed

        scores, id_to_player = Tournament.compute_player_scores(self.current_tournament)
        if not scores:
            print("No players/scores found.")
            return

        # find max score
        max_score = max(scores.values())

        # filter the players with this score
        winner_ids = [pid for pid, sc in scores.items() if sc == max_score]
        winners = [id_to_player[pid] for pid in winner_ids]

        # Display the winner(s)
        if len(winners) == 1:
            # one winner
            winner = winners[0]
            print(
                Style.BRIGHT + Fore.RED +
                f"\n⮞ 🏆 The winner of {self.current_tournament.name} is "
                f"{winner.identifier} : {winner.first_name} {winner.name.upper()} (score {max_score} point(s).\n")
        else:
            # several winners
            print(
                Style.BRIGHT + Fore.RED +
                f"\n⮞ 🏆 The winners of {self.current_tournament.name} are :\n"
            )
            for w in winners:
                print(
                    Style.BRIGHT + Fore.RED +
                    f"   - {w.identifier} : {w.first_name} {w.name.upper()} (tie at {max_score} point(s)).\n"
                )

    def tournament_exists(self, tournament_name):
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
            print(Fore.YELLOW + f"✅ Tournament updated in database !\n{self.current_tournament}")

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
            print(Fore.RED + "⛔ All tournaments are completed. You can not add any score.\n")
        else:

            while True:
                tournament_name = self.view.prompt_for_selecting_tournament(running_tournaments)

                if tournament_name.lower() == "q":
                    return

                tournament = self.get_tournament(tournament_name)

                if tournament.is_completed():
                    self.current_tournament = tournament
                    self.display_completed_tournament()
                    print(Fore.RED + "Tournament already completed ! Please choose another one.\n")
                    continue
                break

            for tournament in self.tournaments:
                if tournament.name == tournament_name:
                    self.current_tournament = tournament
            print(Fore.YELLOW + f"\nSelected tournament: {tournament_name}.")

            if self.current_tournament.current_round < 4:
                # set scores for current round
                self.set_tournament_scores()

                # Set end date/time for current round
                self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

                # update current round
                self.current_tournament.current_round += 1

                # create next round and matches
                self.current_tournament.create_round(self.current_tournament.current_round)

                # Save
                self.save_tournament(tournament_name)

            else:
                # set scores for current round
                self.set_tournament_scores()

                # Set end date/time for current round
                self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

                # Save
                self.save_tournament(tournament_name)

                # Tournament completed
                self.display_completed_tournament()

    def set_tournament_scores(self):
        """
        Method that sets the tournament scores.
        """
        tournament = self.current_tournament
        rnd = tournament.rounds[tournament.current_round - 1]
        print(rnd)
        for match in rnd.matches:
            p1, _, _ = match.match_tuple[0]
            p2, _, _ = match.match_tuple[1]

            score1 = self.view.prompt_for_adding_player_score(p1)
            score2 = 0
            match float(score1):
                case 0:
                    score2 += 1.0
                case 0.5:
                    score2 += 0.5
                case 1.0:
                    score2 += 0.0

            match.set_scores(p1, score1, p2, score2)
        print(Fore.GREEN + f"\nScores saved for {rnd.round_name}.")
        print(rnd)

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
            print(Fore.YELLOW + "❌ Identifier already assigned in database !\n")
        else:
            players.add_player(player)
            if players.save_players_to_json(PLAYERS_DATA_JSON):
                print(Fore.YELLOW + f"✅ New player added to database !\n{player}")

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
        all_players = self.get_players()
        selected_players = Players()

        while current_number < number:
            players_left = number - current_number
            player_identifier = self.view.prompt_for_selecting_players(all_players, players_left, selected_players)
            player = all_players.get_player_by_identifier(player_identifier)

            if player is None:
                print("❌ Player not found. Please try again.\n")
                continue

            if any(p.identifier == player.identifier for p in selected_players):
                print("⚠️ Player already selected. Please choose another one.\n")
                continue

            selected_players.add_player(player)
            current_number += 1
            print(f"✅ {player} added to tournament. ({current_number}/{number}).\n")

        return selected_players

    def display_tournaments_sub_menu(self):
        """
        Method that displays the "update a tournament" sub menu.
        """
        while True:
            self.view.display_update_tournament_menu()
            submenu = self.view.prompt_for_updating_tournament_menu()

            match submenu:
                case 1:
                    self.display_tournaments()
                case 2:
                    self.update_tournament()
                case 3:
                    break

    def display_reports_sub_menu(self):
        while True:
            self.view.display_reports_menu()
            submenu = self.view.prompt_for_reports_menu()

            match int(submenu):
                case 1:
                    self.display_report(1)
                case 2:
                    self.display_report(2)
                case 3:
                    self.display_report(3)
                case 4:
                    self.display_report(4)
                case 5:
                    break

    @staticmethod
    def save_report(path, content):
        try:
            output_path = Path(path)
            output_path.parent.mkdir(exist_ok=True)
            with open(path, "w", encoding="utf-8") as html_file:
                html_file.write(content)
                return True

        except FileNotFoundError:
            print(f"{path} : ❌ file not found !")
            return False

    def display_report(self, report):
        while True:
            answer = self.view.prompt_for_generating_report()
            if answer == "y" or answer == "Y":
                path = Path()
                content = ""
                match report:
                    case 1:
                        content = self.generate_report_alphabetically_players()
                        path = ALPHABETICALLY_PLAYERS_REPORT

                    case 2:
                        content = self.generate_report_tournaments()
                        path = ALL_TOURNAMENTS_REPORT

                    case 3:
                        # Get tournaments
                        tournaments = self.get_all_tournaments()

                        tournament_name = self.view.prompt_for_selecting_tournament(tournaments)
                        print(tournament_name)
                        current_tournament = Tournament("", "")

                        for tournament in tournaments:
                            if tournament.name == tournament_name:
                                current_tournament = tournament

                        content = self.generate_report_current_tournament_players(current_tournament)
                        path = CURRENT_TOURNAMENT_PLAYERS_REPORT

                    case 4:
                        # Get tournaments
                        tournaments = self.get_all_tournaments()

                        tournament_name = self.view.prompt_for_selecting_tournament(tournaments)
                        print(tournament_name)
                        current_tournament = Tournament("", "")

                        for tournament in tournaments:
                            if tournament.name == tournament_name:
                                current_tournament = tournament

                        content = self.generate_report_current_tournament_all_rounds_and_matches(current_tournament)
                        path = CURRENT_TOURNAMENT_ROUNDS_AND_MATCHES_REPORT

                self.save_report(path, content)
                print("The HTML report has been generated.")
                print(f"Here ⯈ {path}\n")
                break

            elif answer == "n" or answer == "N":
                print("Ok, cancelled.")
                break
            else:
                print(Fore.RED + "❌ You must answer yes or no (y/n).")
                continue

    def generate_report_alphabetically_players(self):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(ALPHABETICALLY_PLAYERS_TEMPLATE_HTML)

        # Get players
        players = self.get_players()

        # Sort players alphabetically
        sorted_players = sorted(players, key=lambda p: p.name)

        # Display
        print(f"{len(sorted_players)} players alphabetically sorted.\n")
        print(f"{Players(sorted_players)}\n")

        # Generate HTML report content
        html = template.render(players=sorted_players)

        return html

    def generate_report_tournaments(self):
        # Get tournaments
        tournaments = self.get_all_tournaments()

        # Sort tournaments alphabetically
        sorted_tournaments = sorted(tournaments, key=lambda t: t.name)

        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(TOURNAMENTS_TEMPLATE_HTML)

        # Display
        print(f"{Tournaments(sorted_tournaments)}\n")

        # Generate HTML report content
        html = template.render(tournaments=sorted_tournaments)

        return html

    @staticmethod
    def generate_report_current_tournament_players(tournament):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(CURRENT_TOURNAMENT_PLAYERS_TEMPLATE_HTML)

        # Display
        print(f"\nThe players of selected tournament \"{tournament.name}\":\n")
        for player in tournament.players:
            print(f"{player}")

        sorted_players = sorted(tournament.players, key=lambda p: p.name)
        tournament.players = sorted_players
        # Generate HTML report content
        html = template.render(tournament=tournament)

        return html

    @staticmethod
    def generate_report_current_tournament_all_rounds_and_matches(tournament):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(CURRENT_TOURNAMENT_ROUNDS_MATCHES_TEMPLATE_HTML)

        # Display
        print(f"\nAll the rounds and matches of selected tournament \"{tournament.name}\":\n")
        for rnd in tournament.rounds:
            print(rnd)

        # Generate HTML report content
        html = template.render(tournament=tournament)

        return html


if __name__ == "__main__":

    view = View()
    controller = Controller(view)
    controller.run()
