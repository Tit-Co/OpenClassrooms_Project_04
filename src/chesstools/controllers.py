from .models import Match, Player, Players, Round, Tournament, Tournaments
from .views import View
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)

TOURNAMENT_FOLDER = Path("./data/tournaments/")
TOURNAMENTS_DATA_JSON = TOURNAMENT_FOLDER / Path("./tournaments.json")
PLAYERS_DATA_JSON = TOURNAMENT_FOLDER / Path("./players.json")


class Controller:
    def __init__(self, view):
        # models
        self.current_tournament = None
        self.tournaments = Tournaments()

        # views
        self.view = view

    def run(self):
        """
        Method that runs the controller.
        """
        while True:
            self.view.display_main_menu()
            menu = self.view.prompt_for_main_menu()

            match menu:
                case 1:
                    self.create_tournament()
                case 2:
                    self.display_tournaments_sub_menu()
                case 3:
                    self.add_player_in_database()
                case 4:
                    self.display_players()
                case 5:
                    self.display_tournaments()
                case 6:
                    self.display_reports()
                case 7:
                    print(Style.BRIGHT + Fore.RED + "👋 Goodbye ! 👋")
                    break

    def get_players(self):
        """
        Method that gets players object from the json file
        Returns:
            Players object.
        """
        print(Fore.YELLOW + "⮞ Getting players...\n")
        players = Players()

        # generates random players
        # players.generate_random_players(10)

        # loads players datas from json
        if players.load_players_from_json(PLAYERS_DATA_JSON):
            return players
        else:
            return None

    def get_tournaments(self):
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
            return None

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
        tournaments = self.get_tournaments()
        print(tournaments)

    def create_tournament(self):
        """
        Method that creates a tournament object. Work in progress.
        """
        name = self.view.prompt_for_tournament_name()
        place = self.view.prompt_for_tournament_place()
        start_date = self.view.prompt_for_tournament_start_date()
        end_date = self.view.prompt_for_tournament_end_date()
        description = self.view.prompt_for_tournament_description()
        players_number = self.view.prompt_for_tournament_players_number()
        self.current_tournament = Tournament(name, place, start_date, end_date, players=None, description=description)
        players_to_play = self.select_tournament_players(players_number)

        self.tournaments = self.get_tournaments()
        self.current_tournament.add_players(players_to_play)

        # Tournament starts
        # Create round 1
        self.create_round(self.current_tournament.current_round)

        print(self.current_tournament)

        # Saving to json
        if self.tournaments.tournament_exists(self.current_tournament):
            print(Fore.YELLOW + "❌ Tournament already in the database !\n")
        else:
            self.tournaments.add_tournament(self.current_tournament)
            if self.tournaments.save_tournament_to_json(TOURNAMENTS_DATA_JSON):
                print(Fore.YELLOW + f"✅ New tournament added to database !\n{self.current_tournament}")

    def match_already_played(self, player1, player2):
        """
        Method that checks if the player 1 has already played with player 2.
        Args:
            player1 (Player): Player 1 object.
            player2 (Player): Player 2 object.

        Returns:
            A boolean indicating if the player 1 has already played with player 2.
        """
        for rnd in self.current_tournament.rounds:
            for match in rnd.matches:
                p1 = match.match_tuple[0][0]
                p2 = match.match_tuple[1][0]
                if (p1 == player1 and p2 == player2) or (p1 == player2 and p2 == player1):
                    return True
        return False

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

    def create_round(self, round_number):
        """
        Method that creates a round object.
        Args:
            round_number (int): The round number.
        """
        if round_number == 1:
            # shuffles players
            self.current_tournament.players.shuffle()
        else:
            self.current_tournament.sort_players_by_score()

        # create round
        round_obj = Round(f"Round {round_number}")

        # create matches
        self.create_matches(self.current_tournament.players, round_obj)

        # Set start date/time
        round_obj.set_start_date()

        # Append round to tournament
        self.current_tournament.rounds.append(round_obj)

        print(round_obj)

    def display_completed_tournament(self):
        """
        Method that displays a completed tournament object and th winner of the tournament.
        """
        # Tournament completed
        print("\nTournament completed !\n")

        # sort players by score
        self.current_tournament.sort_players_by_score()
        players = self.current_tournament.players

        # Display the winner
        print(Style.BRIGHT + Fore.RED + f"⮞ The winner of {self.current_tournament.name} is "
                                        f"{players[0].identifier} : "
                                        f"{players[0].name} "
                                        f"{players[0].first_name}.")

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
        self.tournaments = self.get_tournaments()
        tournament_name = self.view.prompt_for_selecting_tournament(self.tournaments)
        for tournament in self.tournaments:
            if tournament.name == tournament_name:
                self.current_tournament = tournament
        print(Fore.YELLOW + f"Selected tournament: {tournament_name}.")

        if not self.current_tournament.is_completed():
            if self.current_tournament.current_round < 4:
                # set scores for current round
                self.set_tournament_scores()

                # Set end date/time for current round
                self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

                # update current round
                self.current_tournament.current_round += 1

                # create next round and matches
                self.create_round(self.current_tournament.current_round)

                # Save
                self.save_tournament(tournament_name)

            else:
                # set scores for current round
                self.set_tournament_scores()

                # Set end date/time for current round
                self.current_tournament.rounds[self.current_tournament.current_round - 1].set_end_date()

                # Set tournament completed boolean to True
                self.current_tournament.completed = True

                # Tournament completed
                self.display_completed_tournament()

                # Save
                self.save_tournament(tournament_name)
        else:
            # Only displaying the winner
            self.display_completed_tournament()

    def set_tournament_scores(self):
        """
        Method that sets the tournament scores.
        """
        tournament = self.current_tournament
        print("Rounds in tournament:", tournament.rounds)
        rnd = tournament.rounds[tournament.current_round - 1]
        print(rnd)
        for match in rnd.matches:
            p1, _, _ = match.match_tuple[0]
            p2, _, _ = match.match_tuple[1]

            score1 = self.view.prompt_for_adding_player_score(p1)
            score2 = self.view.prompt_for_adding_player_score(p2)

            match.set_scores(score1, score2)
        print(f"\nScores saved for {rnd.round_name}.")
        print(rnd)

    def add_player_in_database(self):
        """
        Method that loads the players from the json file, creates a new player object with the datas given
        by the user. The new player datas are also saved in the json file.
        """
        name = self.view.prompt_for_player_name()
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


if __name__ == "__main__":

    view = View()
    controller = Controller(view)
    controller.run()
