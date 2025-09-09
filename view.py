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
        print(Fore.BLUE + "▷▷ 4. Display the club players list")
        print(Fore.BLUE + "▷▷ 5. Quit the app\n")

    def prompt_for_main_menu(self):
        """
        Method that prompts the user to choose the main menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3,4,5) ")
            if len(answer) > 1 or answer.isalpha():
                print("❌ Must be 1 digit.")
                continue
            if int(answer) > 5:
                print("❌ Must be a digit between 1 & 5.")
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
        first_name = input("Enter the player first name: ")
        if not first_name:
            return None
        return first_name

    def prompt_for_player_birth_date(self):
        """
        Method that prompts the user to choose the birthdate.
        Returns:
            The answer converted to datetime.
        """
        while True:
            birth_date = input("Enter birth date (dd/mm/yyyy): ").strip()
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
            if len(identifier) < 5 or len(identifier) > 7:
                print("❌ Must be 2 letters + 5 digits.")
                continue

            # Verifies the first two characters as letters
            if not (identifier[0].isalpha() and identifier[1].isalpha()):
                print("❌ Identifier must start with 2 letters.")
                continue

            # Verifies the rest is digits
            if not identifier[2:].isdigit():
                print("❌ Identifier must end with digits.")
                continue

            return identifier
