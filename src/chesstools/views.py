import sys
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt

console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",  # active la palette complète
    width=200
)

MESSAGE = {"alpha": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be 1 digit.[/bright_red]",
           "empty": "[bold bright_red]❌[/bold bright_red] [bright_red]Empty string.[/bright_red]",
           "invalid": "[bold bright_red]❌[/bold bright_red] [bright_red]You typed a special character.[/bright_red]",
           "digit": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be a digit[/bright_red]",
           "digit_between": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be a digit between[/bright_red]",
           "string": "[bold bright_red]❌[/bold bright_red] [bright_red]You must enter a string.[/bright_red]",
           "invalid_date": "[bold bright_red]❌[/bold bright_red] [bright_red]Invalid date format. "
                           "Please use dd/mm/yyyy.[/bright_red]"}


class MainView:

    @staticmethod
    def display_main_menu():
        """
        Method that displays the main menu screen.
        """
        console.print("[bold bright_red]\n♕ - WELCOME TO CHESS CLUB ! - ♕\n[/bold bright_red]")
        console.print("[bold bright_blue]▶ MAIN MENU ◀[/bold bright_blue]\n")
        console.print("[bright_blue]▷▷ 1. Tournaments[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Players[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Reports[/bright_blue]")
        console.print("[bright_blue]▷▷ 4. Quit the app[/bright_blue]\n")

    @staticmethod
    def prompt_for_main_menu():
        """
        Method that prompts the user to choose an option in the main menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = Prompt.ask("[bright_white]▶ What do you want to do ? (1,2,3,4) [/bright_white]")
            if answer.isalpha():
                console.print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                console.print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                console.print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 4:
                console.print(MESSAGE["digit_between"] + " 1 & 4.")
                continue
            return int(answer)

    @staticmethod
    def display_goodbye():
        console.print("[bold bright_red]👋 Goodbye ! 👋[/bold bright_red]")


class TournamentView:
    @staticmethod
    def display_tournaments_submenu():
        console.print("[bold bright_blue]\n▶ TOURNAMENTS ◀\n[/bold bright_blue]")
        console.print("[bright_blue]▷▷ 1. Create a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Update a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Display a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 4. Display all the tournaments[/bright_blue]")
        console.print("[bright_blue]▷▷ 5. Go back to main menu\n[/bright_blue]")

    @staticmethod
    def display_update_tournament_menu():
        """
        Method that displays the tournament submenu.
        """
        console.print("[bold bright_blue]\n▶ UPDATE A TOURNAMENT ◀\n[/bold bright_blue]")
        console.print("[bright_blue]▷▷ 1. Display all tournaments[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Add scores to a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Go back to main menu\n[/bright_blue]")

    @staticmethod
    def prompt_for_tournaments_submenu():
        """
        Method that prompts the user to choose an option in the main menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = Prompt.ask("[bright_white]▶ What do you want to do ? (1,2,3,4,5) [/bright_white]")
            if answer.isalpha():
                console.print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                console.print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                console.print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 5:
                console.print(MESSAGE["digit_between"] + " 1 & 5.")
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
            answer = Prompt.ask("[bright_white]▶ What do you want to do ? (1,2,3) [/bright_white]")

            if answer.isalpha():
                console.print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                console.print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                console.print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 3:
                console.print(MESSAGE["digit_between"] + " 1 & 3.")
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
            answer = Prompt.ask("[bright_white]▶ What do you want to do ? (1,2,3) [/bright_white]")
            if answer.isalpha():
                console.print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                console.print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                console.print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 3:
                console.print(MESSAGE["digit_between"] + " 1 & 3.")
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
            tournament_name = Prompt.ask("[bright_white]▶ Enter the tournament name (or enter 'q' to go back) "
                                         "[/bright_white]")
            if not tournament_name:
                console.print(MESSAGE["empty"])
                continue
            if tournament_name.isdigit():
                console.print(MESSAGE["string"])
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
            tournament_place = Prompt.ask("[bright_white]▶ Enter the tournament place [/bright_white]")
            if not tournament_place:
                console.print(MESSAGE["empty"])
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
            question = Prompt.ask("[bright_white]▶ Do you want to start the tournament today ? (y/n) "
                                  "[/bright_white]").strip().lower()
            if not question:
                console.print(MESSAGE["empty"])
                continue

            if question in ("y", "yes"):
                today = datetime.today()
                today_fr = today.strftime("%d/%m/%Y")
                return today_fr

            elif question in ("n", "no"):
                while True:
                    tournament_start_date = Prompt.ask("[bright_white]▶ Enter the tournament start date (dd/mm/yyyy) "
                                                       "[/bright_white]").strip()
                    if not tournament_start_date:
                        console.print(MESSAGE["empty"])
                        continue
                    try:
                        datetime.strptime(tournament_start_date, "%d/%m/%Y")
                        return tournament_start_date
                    except ValueError:
                        console.print(MESSAGE["invalid_date"])
            else:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]You must enter 'y' or 'n'."
                              "[/bright_red]")

    @staticmethod
    def prompt_for_tournament_end_date():
        """
        Method that prompts the user to choose the tournament end date.
        Returns:
            The answer converted to datetime.
        """
        while True:
            tournament_end_date = Prompt.ask("[bright_white]▶ Enter the tournament end date (dd/mm/yyyy) "
                                             "[/bright_white]")
            if not tournament_end_date:
                console.print(MESSAGE["empty"])
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(tournament_end_date, "%d/%m/%Y")
                return tournament_end_date
            except ValueError:
                console.print(MESSAGE["invalid_date"])

    @staticmethod
    def prompt_for_tournament_description():
        """
        Method that prompts the user to choose the tournament description.
        Returns:
            The answer converted to str.
        """
        while True:
            tournament_description = Prompt.ask("[bright_white]▶ Enter the tournament description (optional) "
                                                "[/bright_white]")
            if not tournament_description:
                console.print(MESSAGE["empty"])
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
            players_number = Prompt.ask("[bright_white]▶ Enter the tournament players number [/bright_white]")
            if not players_number.isdigit():
                console.print(MESSAGE["digit"])
                continue
            if int(players_number) <= 0:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Must be a positive number."
                              "[/bright_red]")
                continue
            if not int(players_number) % 2 == 0:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Must be an even number."
                              "[/bright_red]")
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
        console.print("\n[bright_white]▶ Select a tournament by typing the name. Here are the available tournaments "
                      "[/bright_white]\n")

        for tournament in tournaments:
            console.print(f"[bright_white]❱❱ {tournament.name}[/bright_white]")
        console.print("\n")
        while True:
            name = self.prompt_for_tournament_name()

            if name.lower() == "q":
                return "q"

            if not self.tournament_exists(name, tournaments):
                console.print(f"[bold bright_red]❌[/bold bright_red] [bright_red]The tournament {name} does not "
                              f"exist.\n[/bright_red]")
                continue
            return name

    @staticmethod
    def display_tournament_name(tournament_name):
        console.print(tournament_name)

    @staticmethod
    def display_tournament(tournament):
        """
        Method that displays tournament object.
        """
        console.print(tournament)

    @staticmethod
    def display_round(rnd):
        console.print(rnd)

    @staticmethod
    def display_tournaments(tournaments):
        """
        Method that displays tournaments object.
        """
        console.print(tournaments)

    @staticmethod
    def display_tournament_name_exists():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]The tournament's name already exists. "
                      "Please choose another one.\n[/bright_red]")

    @staticmethod
    def display_tournament_exists():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Tournament already in the database !\n"
                      "[/bright_red]")

    @staticmethod
    def display_tournament_added(current_tournament):
        console.print("[bright_yellow]✅ New tournament added to database ![/bright_yellow]")
        console.print(current_tournament)

    @staticmethod
    def display_tournament_updated(current_tournament):
        console.print("[bright_yellow]✅ Tournament updated in database ![/bright_yellow]")
        console.print(current_tournament)

    @staticmethod
    def display_all_tournaments_completed():
        console.print("[bright_red]⛔ All tournaments are completed. You can not add any score.\n[/bright_red]")

    @staticmethod
    def display_tournament_completed():
        console.print("[bright_red]Tournament already completed ! Please choose another one.\n[/bright_red]")

    @staticmethod
    def display_selected_tournament(tournament_name):
        console.print(f"[bright_yellow]\nSelected tournament: [/bright_yellow]{tournament_name}.")

    @staticmethod
    def display_tournament_round_score_saved(round_name):
        console.print(f"[bright_green]\nScores saved for[/bright_green] {round_name}.")

    @staticmethod
    def display_player_not_found():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Player not found. Please try again.\n"
                      "[/bright_red]")

    @staticmethod
    def display_player_exists():
        console.print("[bright_white]⚠️ Player already selected. Please choose another one.[/bright_white]\n")

    @staticmethod
    def display_player_added(player, current_number, number):
        console.print(f"{player.__rich_console__(console)}\n✅ [bright_yellow]added to tournament. "
                      f"({current_number}/{number}).\n[/bright_yellow]")

    @staticmethod
    def display_no_scores_found():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]No players/scores found.[/bright_red]")

    @staticmethod
    def display_winners(winners, max_score, tournament_name):
        points = "point" if max_score <= 1 else "points"
        # Display the winner(s)
        if len(winners) == 1:
            # one winner
            winner = winners[0]
            console.print(
                f"\n⮞ 🏆 [bold bright_red]The winner of {tournament_name} is "
                f"{winner.identifier} : {winner.first_name} {winner.name.upper()} (score {max_score} {points}).\n"
                f"[/bold bright_red]")
        else:
            # several winners
            console.print(
                f"\n⮞ 🏆 [bold bright_red]The winners of {tournament_name} are :\n[/bold bright_red]"
            )
            for winner in winners:
                console.print(
                    f"[bold bright_red]   - {winner.identifier} : "
                    f"{winner.first_name} {winner.name.upper()} (tie at {max_score} {points}).\n[/bold bright_red]"
                )


class PlayerView:

    @staticmethod
    def display_players_submenu():
        console.print("[bold bright_blue]\n▶ PLAYERS ◀\n[/bold bright_blue]")
        console.print("[bright_blue]▷▷ 1. Add a player into database[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Display the club players[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Go back to main menu\n[/bright_blue]")

    @staticmethod
    def display_enough_players():
        """
        Method that displays a 'not enough players' message.
        """
        console.print("\n[bright_red]There is not enough players to create a tournament.[/bright_red]\n")

    @staticmethod
    def display_no_players():
        """
        Method that displays a 'no players' message.
        """
        console.print("\n[bright_red]No players found. You can not create a new tournament before adding new players."
                      "[/bright_red]\n")

    @staticmethod
    def prompt_for_players_submenu():
        """
        Method that prompts the user to choose an option in the players submenu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = Prompt.ask("[bright_white]▶ What do you want to do ? (1,2,3) [/bright_white]")
            if answer.isalpha():
                console.print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                console.print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                console.print(MESSAGE["invalid"])
                continue
            elif int(answer) <= 0 or int(answer) > 3:
                console.print(MESSAGE["digit_between"] + " 1 & 3.")
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
            name = Prompt.ask("[bright_white]▶ Enter the player name (or enter 'q' to go back) [/bright_white]")
            if not name:
                console.print(MESSAGE["empty"])
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
            first_name = Prompt.ask("[bright_white]▶ Enter the player first name [/bright_white]")
            if not first_name:
                console.print(MESSAGE["empty"])
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
            birth_date = Prompt.ask("[bright_white]▶ Enter birth date (dd/mm/yyyy) [/bright_white]").strip()
            if not birth_date:
                console.print(MESSAGE["empty"])
                continue
            try:
                # Verifies et converts in datetime object
                datetime.strptime(birth_date, "%d/%m/%Y")
                return birth_date
            except ValueError:
                console.print(MESSAGE["invalid_date"])

    @staticmethod
    def prompt_for_player_identifier():
        """
        Method that prompts the user to choose the player identifier.
        Returns:
            The answer in the appropriate format, 2 letter + 5 digits (ex : AB12345).
        """
        while True:
            identifier = Prompt.ask("[bright_white]▶ Enter the player identifier (ex: AB12345) "
                                    "[/bright_white]").strip()

            # Verify length
            if len(identifier) < 5:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Too short. "
                              "Must be 2 letters + 5 digits.[/bright_red]")
                continue
            if len(identifier) > 7:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Too long. "
                              "Must be 2 letters + 5 digits.[/bright_red]")
                continue

            letters, digits = identifier[:2], identifier[2:]

            if letters.isalpha() and digits.isdigit():
                identifier = letters.upper() + digits
                return identifier
            else:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Invalid format. "
                              "Must be like: AB12345 [/bright_red]")

    @staticmethod
    def display_players(players):
        console.print(players)

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
        console.print("[bright_white]▶ Select a player by typing the identifier (ex: AB12345) [/bright_white]")
        console.print(all_players)

        all_id_str = ""
        for idx, player in enumerate(selected_players, start=1):
            sep = " - " if idx < len(selected_players) else " "
            all_id_str += f"N°{idx} = {player.identifier}{sep}"

        console.print(f"[bright_yellow]⚠️ Number of players to select: {numbers_left} [{all_id_str}]"
                      f"[/bright_yellow]\n")

        while True:
            identifier = self.prompt_for_player_identifier()
            if not self.player_exists(identifier, all_players):
                console.print(f"[bold bright_red]❌[/bold bright_red] [bright_red]Player with identifier "
                              f"{identifier} does not exist.[/bright_red]\n")
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
            score = Prompt.ask(f"\n[bright_white]▶ Enter score for player[/bright_white] {player.identifier}. "
                               f"[bright_white]The score for the other player will be set automatically "
                               f"[/bright_white]")
            if not self.is_float(score):
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Must be a float number (0, 0.5, 1)."
                              "[/bright_red]")
                continue
            if float(score) not in [0, 0.5, 1.0]:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Must be 0 or 0.5 or 1."
                              "[/bright_red]")
                continue
            return float(score)

    @staticmethod
    def display_player_identifier_exists():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]This identifier already assigned in database "
                      "![/bright_red]\n")

    @staticmethod
    def display_player_exists():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]This player already exists in database !"
                      "[/bright_red]\n")

    @staticmethod
    def display_player_added(player):
        console.print(f"[bright_green]✅ New player added to database ![/bright_green]\n"
                      f"{player.__rich_console__(console)}")


class ReportView:

    @staticmethod
    def display_reports_menu():
        """
        Method that displays the reports menu screen.
        """
        console.print("[bold bright_blue]\n▶ REPORTS ◀\n[/bold bright_blue]")
        console.print("[bright_blue]▷▷ 1. Display alphabetically sorted list of players[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Display tournaments' list[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Display a tournament's players list[/bright_blue]")
        console.print("[bright_blue]▷▷ 4. Display all tournament's rounds and matches[/bright_blue]")
        console.print("[bright_blue]▷▷ 5. Go back to main menu\n[/bright_blue]")

    @staticmethod
    def prompt_for_reports_menu():
        """
        Method that prompts the user to choose an option in the reports' menu screen.
        Returns:
            The answer converted to int.
        """
        while True:
            answer = Prompt.ask("[bright_white]▶ What do you want to do ? (1,2,3,4,5) [/bright_white]")
            if len(answer) > 1 or answer.isalpha():
                console.print(MESSAGE["alpha"])
                continue
            elif len(answer) == 0:
                console.print(MESSAGE["empty"])
                continue
            elif not answer.isalpha() and not answer.isdigit():
                console.print(MESSAGE["invalid"])
                continue
            if int(answer) <= 0 or int(answer) > 5:
                console.print(MESSAGE["digit_between"] + " 1 & 5.")
                continue
            return int(answer)

    @staticmethod
    def prompt_for_generating_report():
        """
        Method that prompts the user to choose to generate a report.
        Returns:
            The answer.
        """
        answer = Prompt.ask("\n[bright_white]▶ Do you want to generate the HTML report ? (y/n) [/bright_white]\n")
        return answer

    @staticmethod
    def display_file_not_found(path):
        console.print(f"{path} : [bold bright_red]❌[/bold bright_red] [bright_red]file not found ![/bright_red]")

    @staticmethod
    def display_report_generated(path):
        console.print(f"[bright_white]The HTML report has been generated.\nHere ⯈[/bright_white] {path}\n")

    @staticmethod
    def display_cancelled():
        console.print("[bright_white]Ok, cancelled.[/bright_white]")

    @staticmethod
    def display_yes_no():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]You must answer yes or no (y/n)."
                      "[/bright_red]")

    @staticmethod
    def display_sorted_players(number, players):
        console.print(f"{number} [bright_white]players alphabetically sorted.[/bright_white]\n")
        console.print(f"{players}\n")

    @staticmethod
    def display_sorted_tournaments(tournaments):
        console.print(f"{tournaments}\n")

    @staticmethod
    def display_selected_tournament_title(tournament_name):
        console.print(f"\n[bright_white]The players of selected tournament[/bright_white] \"{tournament_name}\":\n")

    @staticmethod
    def display_player(player):
        console.print(player)

    @staticmethod
    def display_rnd(rnd):
        console.print(rnd)

    @staticmethod
    def display_all_rounds_and_matches_title(tournament_name):
        console.print(f"\n[bright_white]All the rounds and matches of selected tournament[/bright_white] "
                      f"\"{tournament_name}\":\n")

    @staticmethod
    def display_invalid_report_number():
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Invalid report number.[/bright_red]")
