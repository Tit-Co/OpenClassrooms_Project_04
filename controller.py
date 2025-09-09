from models import Player, Players, Round, Tournament, NUMBER_OF_ROUNDS
from view import View
from pathlib import Path
from colorama import Fore, Style, init
init(autoreset=True)

TOURNAMENT_FOLDER = Path("./data/tournaments/")
TOURNAMENTS_DATA_JSON = TOURNAMENT_FOLDER / Path("./tournaments.json")
PLAYERS_DATA_JSON = TOURNAMENT_FOLDER / Path("./players.json")


class Controller:
    def __init__(self, view):
        # models
        self.matches = []
        self.tournament = None

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
                    pass
                case 2:
                    pass
                case 3:
                    self.add_player()
                case 4:
                    self.display_players()
                case 5:
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
        players.load_players_from_json(PLAYERS_DATA_JSON)
        return players

    def display_players(self):
        """
        Method that displays players object.
        """
        players = self.get_players()
        print(players)

    def create_tournament(self):
        """
        Method that creates a tournament object. Work in progress.
        """
        self.tournament = Tournament("Chess Masters 2000",
                                     "Montreuil",
                                     "08/09/2025",
                                     "09/09/2025",
                                     "Le combat des chefs")

        self.tournament.add_players(self.get_players())
        print(self.tournament)

        for _ in range(self.tournament.rounds_number):
            if self.tournament.current_round == 1:
                # shuffles players
                self.tournament.players.shuffle()

                # creates round
                tournament_round = Round("Round " + str(self.tournament.current_round))
                # creates matches
                tournament_round.create_matches(self.tournament.players)
                print(tournament_round)
                tournament_round.set_start_date()

                # ask user the scores
                # ...

                # specifies scores
                tournament_round.specify_random_scores()

            else:
                # sorts players by score
                self.tournament.sort_players_by_score(verbose=True)

                # creates round
                tournament_round = Round("Round " + str(self.tournament.current_round))
                # creates matches
                tournament_round.create_matches(self.tournament.players)
                print(tournament_round)

                # ask user the scores
                # ...

                # specify the scores
                tournament_round.specify_random_scores()

            print(Fore.YELLOW + "⮞ Matches completed !\n")
            tournament_round.set_end_date()
            print(tournament_round)
            self.tournament.add_round(tournament_round)
            self.tournament.current_round += 1

        # self.players.save_players_to_json(PLAYERS_DATA_JSON)

    def add_player(self):
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
            players.save_players_to_json(PLAYERS_DATA_JSON)
            print(Fore.YELLOW + f"✅ New player added to database !\n{player}")

    def create_rounds(self):
        pass

    def create_matches(self):
        print(Fore.YELLOW + "⮞ Creating matches...\n")

if __name__ == "__main__":

    view = View()
    controller = Controller(view)
    controller.run()
