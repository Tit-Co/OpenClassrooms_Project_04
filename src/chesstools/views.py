from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)


class View:

    @staticmethod
    def display_main_menu():
        """
        Method that displays the main menu screen.
        """
        print(Style.BRIGHT + Fore.RED + "\n♕ - WELCOME TO CHESS CLUB ! - ♕\n")
        print(Style.BRIGHT + Fore.BLUE + "▶ MAIN MENU ◀\n")
        print(Fore.BLUE + "▷▷ 1. Create a tournament")
        print(Fore.BLUE + "▷▷ 2. Update a tournament")
        print(Fore.BLUE + "▷▷ 3. Add a player into database")
        print(Fore.BLUE + "▷▷ 4. Display the club players")
        print(Fore.BLUE + "▷▷ 5. Display a tournament")
        print(Fore.BLUE + "▷▷ 6. Display all the tournaments")
        print(Fore.BLUE + "▷▷ 7. Generate reports")
        print(Fore.BLUE + "▷▷ 8. Quit the app\n")

    @staticmethod
    def display_reports_menu():
        """
        Method that displays the reports menu screen.
        """
        print(Style.BRIGHT + Fore.BLUE + "\n▶ REPORTS ◀\n")
        print(Fore.BLUE + "▷▷ 1. Display alphabetically sorted list of players")
        print(Fore.BLUE + "▷▷ 2. Display tournaments' list")
        print(Fore.BLUE + "▷▷ 3. Display a tournament's players list")
        print(Fore.BLUE + "▷▷ 4. Display all tournament's rounds and matches")
        print(Fore.BLUE + "▷▷ 5. Go back to main menu\n")

    @staticmethod
    def display_update_tournament_menu():
        """
        Method that displays the tournament submenu.
        """
        print(Style.BRIGHT + Fore.BLUE + "\n▶ UPDATE A TOURNAMENT ◀\n")
        print(Fore.BLUE + "▷▷ 1. Display all tournaments")
        print(Fore.BLUE + "▷▷ 2. Add scores to a tournament")
        print(Fore.BLUE + "▷▷ 3. Go back to main menu\n")

    @staticmethod
    def prompt_for_main_menu():
        """
        Method that prompts the user to choose an option in the main menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3,4,5,6,7,8) ")
            if len(answer) > 1 or answer.isalpha():
                print("❌ Must be 1 digit.")
                continue
            if int(answer) <= 0 or int(answer) > 8:
                print("❌ Must be a digit between 1 & 8.")
                continue
            return int(answer)

    @staticmethod
    def prompt_for_reports_menu():
        """
        Method that prompts the user to choose an option in the reports' menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3,4,5) ")
            if len(answer) > 1 or answer.isalpha():
                print("❌ Must be 1 digit.")
                continue
            if int(answer) <= 0 or int(answer) > 5:
                print("❌ Must be a digit between 1 & 5.")
                continue
            return int(answer)

    @staticmethod
    def prompt_for_updating_tournament_menu():
        """
        Method that prompts the user to choose an option in the tournament's update submenu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3) ")
            if len(answer) > 1 or answer.isalpha():
                print("❌ Must be 1 digit.")
                continue
            if int(answer) <= 0 or int(answer) > 3:
                print("❌ Must be a digit between 1 & 3.")
                continue
            return int(answer)

    @staticmethod
    def prompt_for_updating_tournament_scores_menu():
        """
        Method that prompts the user to choose an option in the tournament's scores submenu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3) ")
            if len(answer) > 1 or answer.isalpha():
                print("❌ Must be 1 digit.")
                continue
            if int(answer) <= 0 or int(answer) > 3:
                print("❌ Must be a digit between 1 & 3.")
                continue
            return int(answer)

    @staticmethod
    def prompt_for_player_name():
        """
        Method that prompts the user to choose the player name.
        Returns:
            The answer converted to str.
        """
        while True:
            name = input("▶ Enter the player name: ")
            if not name:
                print("❌ Empty string.")
                continue
            return name

    @staticmethod
    def prompt_for_player_first_name():
        """
        Method that prompts the user to choose the player first name.
        Returns:
            The answer converted to str.
        """
        while True:
            first_name = input("▶ Enter the player first name: ")
            if not first_name:
                print("❌ Empty string.")
                continue
            return first_name

    @staticmethod
    def prompt_for_player_birth_date():
        """
        Method that prompts the user to choose the birthdate.
        Returns:
            The answer converted to datetime.
        """
        while True:
            birth_date = input("▶ Enter birth date (dd/mm/yyyy): ").strip()
            if not birth_date:
                print("❌ Empty string.")
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(birth_date, "%d/%m/%Y")
                return birth_date
            except ValueError:
                print("❌ Invalid date format. Please use dd/mm/yyyy.")

    @staticmethod
    def prompt_for_player_identifier():
        """
        Method that prompts the user to choose the player identifier.
        Returns:
            The answer in the appropriate format, 2 letter + 5 digits (ex : AB12345).
        """
        while True:
            identifier = input("▶ Enter the player identifier (ex: AB12345): ").strip()

            # Verify length
            if len(identifier) < 5:
                print("❌ Too short. Must be 2 letters + 5 digits.")
                continue
            if len(identifier) > 7:
                print("❌ Too long. Must be 2 letters + 5 digits.")
                continue

            letters, digits = identifier[:2], identifier[2:]

            if letters.isalpha() and digits.isdigit():
                identifier = letters.upper() + digits
                return identifier
            else:
                print("❌ Invalid format. Must be like: AB12345")

    @staticmethod
    def prompt_for_tournament_name():
        """
        Method that prompts the user to choose the tournament name.
        Returns:
            The answer converted to str.
        """
        while True:
            tournament_name = input("▶ Enter the tournament name: ")
            if not tournament_name:
                print("❌ Empty string.")
                continue
            if tournament_name.isdigit():
                print("❌ You must enter a string.")
                continue
            return tournament_name

    @staticmethod
    def prompt_for_tournament_place():
        """
        Method that prompts the user to choose the tournament place.
        Returns:
            The answer converted to str.
        """
        while True:
            tournament_place = input("▶ Enter the tournament place: ")
            if not tournament_place:
                print("❌ Empty string.")
                continue
            return tournament_place

    @staticmethod
    def prompt_for_tournament_start_date():
        """
        Method that prompts the user to choose the tournament start date.
        Returns:
            The answer converted to datetime.
        """
        while True:
            question = input("▶ Do you want to start the tournament today ? (y/n) ").strip().lower()
            if not question:
                print("❌ Empty string.")
                continue

            if question in ("y", "yes"):
                today = datetime.today()
                today_fr = today.strftime("%d/%m/%Y")
                return today_fr

            elif question in ("n", "no"):
                while True:
                    tournament_start_date = input("▶ Enter the tournament start date (dd/mm/yyyy): ").strip()
                    if not tournament_start_date:
                        print("❌ Empty string.")
                        continue
                    try:
                        datetime.strptime(tournament_start_date, "%d/%m/%Y")
                        return tournament_start_date
                    except ValueError:
                        print("❌ Invalid date format. Please use dd/mm/yyyy.")
            else:
                print("❌ You must enter 'y' or 'n'.")

    @staticmethod
    def prompt_for_tournament_end_date():
        """
        Method that prompts the user to choose the tournament end date.
        Returns:
            The answer converted to datetime.
        """
        while True:
            tournament_end_date = input("▶ Enter the tournament end date (dd/mm/yyyy): ")
            if not tournament_end_date:
                print("❌ Empty string.")
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(tournament_end_date, "%d/%m/%Y")
                return tournament_end_date
            except ValueError:
                print("❌ Invalid date format. Please use dd/mm/yyyy.")

    @staticmethod
    def prompt_for_tournament_description():
        """
        Method that prompts the user to choose the tournament description.
        Returns:
            The answer converted to str.
        """
        while True:
            tournament_description = input("▶ Enter the tournament description (optional): ")
            if not tournament_description:
                print("❌ Empty string.")
                continue
            return tournament_description

    @staticmethod
    def prompt_for_tournament_players_number():
        """
        Method that prompts the user to choose the tournament players number.
        Returns:
            The answer converted to int.
        """
        while True:
            players_number = input("▶ Enter the tournament players number : ")
            if not players_number.isdigit():
                print("❌ Must be a digit.")
                continue
            if int(players_number) <= 0:
                print("❌ Must be a positive number.")
                continue
            if not int(players_number) % 2 == 0:
                print("❌ Must be an even number.")
                continue
            return players_number

    @staticmethod
    def player_exists(identifier, players):
        """
        Method that checks if a player, identified by his identifier, exists in a players object.
        Args:
            identifier (str): The player's identifier.
            players (Players): The players object.

        Returns:
            A boolean. True if the player exists, False otherwise.
        """
        for p in players:
            if identifier == p.identifier:
                return True
        return False

    @staticmethod
    def tournament_exists(name, tournaments):
        """
        Method that checks if a tournament, identified by his name, exists in a tournaments object.
        Args:
            name (str): The tournament's name.
            tournaments (Tournaments): The tournaments object.

        Returns:
            A boolean. True if the tournament exists, False otherwise.
        """
        for t in tournaments:
            if name == t.name:
                return True
        return False

    def prompt_for_selecting_players(self, all_players, numbers_left, selected_players):
        """
        Method that prompts the user to choose the players.
        Args:
            all_players (Players):  Players object.
            numbers_left (int):  Number of players left to select.
            selected_players (Players): selected players object.

        Returns:
            The player identifier in string format.
        """
        print("▶ Select a player by typing the identifier (ex: AB12345): ")
        print(all_players)

        all_id_str = ""
        for idx, player in enumerate(selected_players, start=1):
            sep = " - " if idx < len(selected_players) else " "
            all_id_str += f"N°{idx} = {player.identifier}{sep}"

        print(Fore.YELLOW + f"⚠️ Number of players to select: {numbers_left} [{all_id_str}]\n")

        while True:
            identifier = self.prompt_for_player_identifier()
            if not self.player_exists(identifier, all_players):
                print(f"❌ Player with identifier {identifier} does not exist.\n")
                continue
            return identifier

    def prompt_for_selecting_tournament(self, tournaments):
        """
        Method that prompts the user to choose the tournament.
        Args:
            tournaments (Tournaments): Tournaments object.

        Returns:
            The tournament name in string format.
        """
        print("\n▶ Select a tournament by typing the name. Here are the available tournaments:\n")

        for tournament in tournaments:
            print(f"❱❱ {tournament.name}")
        print("\n")
        while True:
            name = self.prompt_for_tournament_name()
            if not self.tournament_exists(name, tournaments):
                print(f"❌ The tournament {name} does not exist.\n")
                continue
            return name

    @staticmethod
    def is_float(value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def prompt_for_adding_player_score(self, player):
        """
        Method that prompts the user to add the player score.
        Args:
            player (Player): Player object.

        Returns:
            The score in float format.
        """
        while True:
            score = input(f"\n▶ Enter score for player {player.identifier}. "
                          f"The score for the other player will be set automatically : ")
            if not self.is_float(score):
                print("❌ Must be a float number (0, 0.5, 1).")
                continue
            if float(score) not in [0, 0.5, 1.0]:
                print("❌ Must be 0 or 0.5 or 1.")
                continue
            return float(score)

    @staticmethod
    def prompt_for_generating_report():
        """
        Method that prompts the user to choose to generate a report.
        Returns:
            The answer.
        """
        answer = input("\n▶ Do you want to generate the HTML report ? (y/n) :\n")
        return answer
