from datetime import datetime

from colorama import Fore, Style, init

init(autoreset=True)

MESSAGE = {"alpha": "❌ Must be 1 digit.",
           "empty": "❌ Empty string.",
           "invalid": "❌ You typed a special character.",
           "digit": "❌ Must be a digit",
           "digit_between": "❌ Must be a digit between",
           "string": "❌ You must enter a string.",
           "invalid_date": "❌ Invalid date format. Please use dd/mm/yyyy."}


class MainView:

    @staticmethod
    def display_main_menu():
        """
        Method that displays the main menu screen.
        """
        print(Style.BRIGHT + Fore.RED + "\n♕ - WELCOME TO CHESS CLUB ! - ♕\n")
        print(Style.BRIGHT + Fore.BLUE + "▶ MAIN MENU ◀\n")
        print(Fore.BLUE + "▷▷ 1. Tournaments")
        print(Fore.BLUE + "▷▷ 2. Players")
        print(Fore.BLUE + "▷▷ 3. Reports")
        print(Fore.BLUE + "▷▷ 4. Quit the app\n")

    @staticmethod
    def prompt_for_main_menu():
        """
        Method that prompts the user to choose an option in the main menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3,4) ")
            if len(answer) > 1 or answer.isalpha():
                print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 4:
                print(MESSAGE["digit_between"] + " 1 & 4.")
                continue
            return int(answer)

    @staticmethod
    def display_goodbye():
        print(Style.BRIGHT + Fore.RED + "👋 Goodbye ! 👋")


class TournamentView:
    @staticmethod
    def display_tournaments_submenu():
        print(Style.BRIGHT + Fore.BLUE + "\n▶ TOURNAMENTS ◀\n")
        print(Fore.BLUE + "▷▷ 1. Create a tournament")
        print(Fore.BLUE + "▷▷ 2. Update a tournament")
        print(Fore.BLUE + "▷▷ 3. Display a tournament")
        print(Fore.BLUE + "▷▷ 4. Display all the tournaments")
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
    def prompt_for_tournaments_submenu():
        """
        Method that prompts the user to choose an option in the main menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3,4,5) ")
            if len(answer) > 1 or answer.isalpha():
                print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 5:
                print(MESSAGE["digit_between"] + " 1 & 5.")
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
                print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 3:
                print(MESSAGE["digit_between"] + " 1 & 3.")
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
                print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 3:
                print(MESSAGE["digit_between"] + " 1 & 3.")
                continue
            return int(answer)

    @staticmethod
    def prompt_for_tournament_name():
        """
        Method that prompts the user to choose the tournament name.
        Returns:
            The answer converted to str.
        """
        while True:
            tournament_name = input("▶ Enter the tournament name (or enter 'q' to go back) : ")
            if not tournament_name:
                print(MESSAGE["empty"])
                continue
            if tournament_name.isdigit():
                print(MESSAGE["string"])
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
                print(MESSAGE["empty"])
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
                print(MESSAGE["empty"])
                continue

            if question in ("y", "yes"):
                today = datetime.today()
                today_fr = today.strftime("%d/%m/%Y")
                return today_fr

            elif question in ("n", "no"):
                while True:
                    tournament_start_date = input("▶ Enter the tournament start date (dd/mm/yyyy): ").strip()
                    if not tournament_start_date:
                        print(MESSAGE["empty"])
                        continue
                    try:
                        datetime.strptime(tournament_start_date, "%d/%m/%Y")
                        return tournament_start_date
                    except ValueError:
                        print(MESSAGE["invalid_date"])
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
                print(MESSAGE["empty"])
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(tournament_end_date, "%d/%m/%Y")
                return tournament_end_date
            except ValueError:
                print(MESSAGE["invalid_date"])

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
                print(MESSAGE["empty"])
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
                print(MESSAGE["digit"])
                continue
            if int(players_number) <= 0:
                print("❌ Must be a positive number.")
                continue
            if not int(players_number) % 2 == 0:
                print("❌ Must be an even number.")
                continue
            return players_number

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

            if name.lower() == "q":
                return "q"

            if not self.tournament_exists(name, tournaments):
                print(f"❌ The tournament {name} does not exist.\n")
                continue
            return name

    @staticmethod
    def display_tournament_name_exists():
        print("❌ The tournament's name already exists. Please choose another one.\n")

    @staticmethod
    def display_tournament_exists():
        print(Fore.YELLOW + "❌ Tournament already in the database !\n")

    @staticmethod
    def display_tournament_added(current_tournament):
        print(Fore.YELLOW + f"✅ New tournament added to database !\n{current_tournament}")

    @staticmethod
    def display_tournament_updated(current_tournament):
        print(Fore.YELLOW + f"✅ Tournament updated in database !\n{current_tournament}")

    @staticmethod
    def display_all_tournaments_completed():
        print(Fore.RED + "⛔ All tournaments are completed. You can not add any score.\n")

    @staticmethod
    def display_tournament_completed():
        print(Fore.RED + "Tournament already completed ! Please choose another one.\n")

    @staticmethod
    def display_selected_tournament(tournament_name):
        print(Fore.YELLOW + f"\nSelected tournament: {tournament_name}.")

    @staticmethod
    def display_tournament_round_score_saved(round_name):
        print(Fore.GREEN + f"\nScores saved for {round_name}.")

    @staticmethod
    def display_player_not_found():
        print("❌ Player not found. Please try again.\n")

    @staticmethod
    def display_player_exists():
        print("⚠️ Player already selected. Please choose another one.\n")

    @staticmethod
    def display_player_added(player, current_number, number):
        print(f"✅ {player} added to tournament. ({current_number}/{number}).\n")

    @staticmethod
    def display_winners(winners, max_score, tournament_name):
        # Display the winner(s)
        if len(winners) == 1:
            # one winner
            winner = winners[0]
            print(
                Style.BRIGHT + Fore.RED +
                f"\n⮞ 🏆 The winner of {tournament_name} is "
                f"{winner.identifier} : {winner.first_name} {winner.name.upper()} (score {max_score} point(s).\n")
        else:
            # several winners
            print(
                Style.BRIGHT + Fore.RED +
                f"\n⮞ 🏆 The winners of {tournament_name} are :\n"
            )
            for winner in winners:
                print(
                    Style.BRIGHT + Fore.RED +
                    f"   - {winner.identifier} : "
                    f"{winner.first_name} {winner.name.upper()} (tie at {max_score} point(s)).\n"
                )


class PlayerView:

    @staticmethod
    def display_players_submenu():
        print(Style.BRIGHT + Fore.BLUE + "\n▶ PLAYERS ◀\n")
        print(Fore.BLUE + "▷▷ 1. Add a player into database")
        print(Fore.BLUE + "▷▷ 2. Display the club's players")
        print(Fore.BLUE + "▷▷ 3. Go back to main menu\n")

    @staticmethod
    def display_enough_players():
        """
        Method that displays a 'not enough players' message.
        """
        print(Fore.RED + "\nThere is not enough players to create a tournament.\n")

    @staticmethod
    def display_no_players():
        """
        Method that displays a 'no players' message.
        """
        print(Fore.RED + "\nNo players found. "
                         "You can not create a new tournament before adding new players.\n")

    @staticmethod
    def prompt_for_players_submenu():
        """
        Method that prompts the user to choose an option in the players submenu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3) ")
            if len(answer) > 1 or answer.isalpha():
                print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 3:
                print(MESSAGE["digit_between"] + " 1 & 3.")
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
            name = input("▶ Enter the player name (or enter 'q' to go back) : ")
            if not name:
                print(MESSAGE["empty"])
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
                print(MESSAGE["empty"])
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
                print(MESSAGE["empty"])
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(birth_date, "%d/%m/%Y")
                return birth_date
            except ValueError:
                print(MESSAGE["invalid_date"])

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

    @staticmethod
    def is_float(value: str) -> bool:
        """
        Method that checks if a value is a float.
        Args:
            value (str): The value to check.

        Returns:
            A boolean. True if the value is a float, False otherwise.
        """
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
    def display_player_exists():
        print(Fore.YELLOW + "❌ Identifier already assigned in database !\n")

    @staticmethod
    def display_player_added(player):
        print(Fore.YELLOW + f"✅ New player added to database !\n{player}")


class ReportView:

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
    def prompt_for_reports_menu():
        """
        Method that prompts the user to choose an option in the reports' menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = input(Style.BRIGHT + "▶ What do you want to do ? (1,2,3,4,5) ")
            if len(answer) > 1 or answer.isalpha():
                print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                print(MESSAGE["invalid"])
                continue
            if int(answer) <= 0 or int(answer) > 5:
                print(MESSAGE["digit_between"] + " 1 & 5.")
                continue
            return int(answer)

    @staticmethod
    def prompt_for_generating_report():
        """
        Method that prompts the user to choose to generate a report.
        Returns:
            The answer.
        """
        answer = input("\n▶ Do you want to generate the HTML report ? (y/n) :\n")
        return answer

    @staticmethod
    def display_file_not_found(path):
        print(f"{path} : ❌ file not found !")

    @staticmethod
    def display_report_generated(path):
        print(f"The HTML report has been generated.\nHere ⯈ {path}\n")

    @staticmethod
    def display_cancelled():
        print("Ok, cancelled.")

    @staticmethod
    def display_yes_no():
        print(Fore.RED + "❌ You must answer yes or no (y/n).")

    @staticmethod
    def display_sorted_players(number, players):
        print(f"{number} players alphabetically sorted.\n")
        print(f"{players}\n")

    @staticmethod
    def display_sorted_tournaments(tournaments):
        print(f"{tournaments}\n")

    @staticmethod
    def display_selected_tournament_title(tournament_name):
        print(f"\nThe players of selected tournament \"{tournament_name}\":\n")

    @staticmethod
    def display_player(player):
        print(player)

    @staticmethod
    def display_rnd(rnd):
        print(rnd)

    @staticmethod
    def display_all_rounds_and_matches_title(tournament_name):
        print(f"\nAll the rounds and matches of selected tournament \"{tournament_name}\":\n")

    @staticmethod
    def display_invalid_report_number():
        print("❌ Invalid report number.")
