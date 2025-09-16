from datetime import datetime
from colorama import Fore, Style, init
init(autoreset=True)


class View:

    def display_main_menu(self):
        """
        Method that displays the main menu screen.
        """
        print(Style.BRIGHT + Fore.RED + "\n♕ - WELCOME TO CHESS CLUB ! - ♕\n")
        print(Style.BRIGHT + Fore.BLUE + "▶ MAIN MENU ◀\n")
        print(Fore.BLUE + "▷▷ 1. Create a tournament")
        print(Fore.BLUE + "▷▷ 2. Update a tournament")
        print(Fore.BLUE + "▷▷ 3. Add a player into database")
        print(Fore.BLUE + "▷▷ 4. Display the club players")
        print(Fore.BLUE + "▷▷ 5. Display the tournaments")
        print(Fore.BLUE + "▷▷ 6. Display reports")
        print(Fore.BLUE + "▷▷ 7. Quit the app\n")

    def display_update_tournament_menu(self):
        """
        Method that displays the tournament submenu.
        """
        print(Style.BRIGHT + Fore.BLUE + "\n▶ UPDATE A TOURNAMENT ◀\n")
        print(Fore.BLUE + "▷▷ 1. Display all tournaments")
        print(Fore.BLUE + "▷▷ 2. Add scores to a tournament")
        print(Fore.BLUE + "▷▷ 3. Go back to main menu\n")

    def display_add_tournament_scores_menu(self):
        """
        Method that displays the tournament scores submenu.
        """
        print(Style.BRIGHT + Fore.BLUE + "\n▶ ADD TOURNAMENT SCORES◀\n")

    def prompt_for_main_menu(self):
        """
        Method that prompts the user to choose an option in the main menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3,4,5,6,7) ")
            if len(answer) > 1 or answer.isalpha():
                print("❌ Must be 1 digit.")
                continue
            if int(answer) <= 0 or int(answer) > 7:
                print("❌ Must be a digit between 1 & 6.")
                continue
            return int(answer)

    def prompt_for_updating_tournament_menu(self):
        """
        Method that prompts the user to choose an option in the tournament scores submenu screen.
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

    def prompt_for_updating_tournament_scores_menu(self):
        """
        Method that prompts the user to choose an option in the tournament submenu screen.
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

    def prompt_for_player_name(self):
        """
        Method that prompts the user to choose the player name.
        Returns:
            The answer converted to str.
        """
        name = input("Enter the player name: ")
        if not name:
            return None
        return name

    def prompt_for_player_first_name(self):
        """
        Method that prompts the user to choose the player first name.
        Returns:
            The answer converted to str.
        """
        while True:
            first_name = input("Enter the player first name: ")
            if not first_name:
                print("❌ Empty string.")
                continue
            return first_name

    def prompt_for_player_birth_date(self):
        """
        Method that prompts the user to choose the birthdate.
        Returns:
            The answer converted to datetime.
        """
        while True:
            birth_date = input("Enter birth date (dd/mm/yyyy): ").strip()
            if not birth_date:
                print("❌ Empty string.")
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(birth_date, "%d/%m/%Y")
                return birth_date
            except ValueError:
                print("❌ Invalid date format. Please use dd/mm/yyyy.")

    def prompt_for_player_identifier(self):
        """
        Method that prompts the user to choose the player identifier.
        Returns:
            The answer in the appropriate format, 2 letter + 5 digits (ex : AB12345).
        """
        while True:
            identifier = input("Enter the player identifier (ex: AB12345): ").strip()

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

    def prompt_for_tournament_name(self):
        """
        Method that prompts the user to choose the tournament name.
        Returns:
            The answer converted to str.
        """
        while True:
            tournament_name = input("Enter the tournament name: ")
            if not tournament_name:
                print("❌ Empty string.")
                continue
            return tournament_name

    def prompt_for_tournament_place(self):
        """
        Method that prompts the user to choose the tournament place.
        Returns:
            The answer converted to str.
        """
        while True:
            tournament_place = input("Enter the tournament place: ")
            if not tournament_place:
                print("❌ Empty string.")
                continue
            return tournament_place

    def prompt_for_tournament_start_date(self):
        """
        Method that prompts the user to choose the tournament start date.
        Returns:
            The answer converted to datetime.
        """
        while True:
            tournament_start_date = input("Enter the tournament start date (dd/mm/yyyy): ")
            if not tournament_start_date:
                print("❌ Empty string.")
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(tournament_start_date, "%d/%m/%Y")
                return tournament_start_date
            except ValueError:
                print("❌ Invalid date format. Please use dd/mm/yyyy.")

    def prompt_for_tournament_end_date(self):
        """
        Method that prompts the user to choose the tournament end date.
        Returns:
            The answer converted to datetime.
        """
        while True:
            tournament_end_date = input("Enter the tournament start date (dd/mm/yyyy): ")
            if not tournament_end_date:
                print("❌ Empty string.")
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(tournament_end_date, "%d/%m/%Y")
                return tournament_end_date
            except ValueError:
                print("❌ Invalid date format. Please use dd/mm/yyyy.")

    def prompt_for_tournament_description(self):
        """
        Method that prompts the user to choose the tournament description.
        Returns:
            The answer converted to str.
        """
        tournament_description = input("Enter the tournament description (optional): ")
        return tournament_description

    def prompt_for_tournament_players_number(self):
        """
        Method that prompts the user to choose the tournament players number.
        Returns:
            The answer converted to int.
        """
        while True:
            players_number = input("Enter the tournament players number : ")
            if not players_number.isdigit():
                print("❌ Must be a digit.")
                continue
            if int(players_number) <= 0:
                print("Must be a positive number.")
                continue
            if not int(players_number) % 2 == 0:
                print("Must be an even number.")
                continue
            return players_number

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
        print("Select a player by typing the identifier (ex: AB12345): ")
        print(all_players)
        all_id_str = ""
        counter = 0
        for player in selected_players:
            if counter < numbers_left:
                all_id_str += f"{player.identifier} - "
            else:
                all_id_str += f"{player.identifier}"
        print(f"Players to select : {str(numbers_left)} [{all_id_str}]\n")
        identifier = self.prompt_for_player_identifier()
        return identifier

    def prompt_for_selecting_tournament(self, all_tournaments):
        """
        Method that prompts the user to choose the tournament.
        Args:
            all_tournaments (Tournaments): Tournaments object.

        Returns:
            The tournament name in string format.
        """
        print("Select a tournament by typing the name : ")
        print(all_tournaments)
        name = self.prompt_for_tournament_name()
        return name

    def prompt_for_adding_player_score(self, player):
        """
        Method that prompts the user to add the player score.
        Args:
            player (Player): Player object.

        Returns:
            The score in float format.
        """
        score = input(f"Enter score for player {player.identifier} : ")
        return float(score)
