import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.chesstools.models import Match, Player, Round, Tournament

console = Console(
    file=sys.stdout,
    force_terminal=True,
    color_system="truecolor",
    width=200
)

MESSAGE = {"alpha": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be 1 digit.[/bright_red]",
           "empty": "[bold bright_red]❌[/bold bright_red] [bright_red]Empty string.[/bright_red]",
           "invalid": "[bold bright_red]❌[/bold bright_red] [bright_red]You typed a special character.[/bright_red]",
           "digit": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be a digit[/bright_red]",
           "digit_between": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be a digit between[/bright_red]",
           "digit_minimum": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be a minimum of 4[/bright_red]",
           "not_even": "[bold bright_red]❌[/bold bright_red] [bright_red]Must be an even number[/bright_red]",
           "string": "[bold bright_red]❌[/bold bright_red] [bright_red]You must enter a string.[/bright_red]",
           "invalid_date": "[bold bright_red]❌[/bold bright_red] [bright_red]Invalid date format. "
                           "Please use dd/mm/yyyy.[/bright_red]"}


class MainView:
    @staticmethod
    def display_main_menu() -> None:
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
    def prompt_for_main_menu() -> int:
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
    def display_goodbye() -> None:
        """
        Method that displays a goodbye message.
        """
        console.print("[bold bright_red]👋 Goodbye ! 👋[/bold bright_red]")


class TournamentView:
    @staticmethod
    def display_match_details(match: Match) -> Group:
        """
        Method that displays the match details.
        Args:
            match (Match): The match object.

        Returns:
            Group: The match details in Rich format.
        """
        player_1, score_1, color_1 = match.match_tuple[0]
        player_2, score_2, color_2 = match.match_tuple[1]

        score_1_display = str(score_1) if score_1 is not None else "0"
        score_2_display = str(score_2) if score_2 is not None else "0"

        prefix = "[bold bright_white]┝╍ [/bold bright_white]"
        color_1_ = f"[bright_white]{color_1.upper()}[/bright_white]"
        color_2_ = f"[bright_white]{color_2.upper()}[/bright_white]"
        sep = " color : "
        score_text = " score : "

        table_1 = Table(show_header=False, border_style="black")
        table_1.add_column("Prefix", justify="center")
        table_1.add_column("Player", justify="center")
        table_1.add_column("Color", justify="center")
        table_1.add_column("Score Text", justify="center")
        table_1.add_column("Score", justify="center")
        table_1.add_row(prefix,
                        PlayerView.display_player_details(player_1),
                        sep,
                        color_1_,
                        score_text,
                        score_1_display)

        table_vs = Table(show_header=False, border_style="black")
        table_vs.add_column("VS", justify="center")
        table_vs.add_row("[bold yellow]VS[/bold yellow]")

        table_2 = Table(show_header=False, border_style="black")
        table_2.add_column("Prefix", justify="center")
        table_2.add_column("Player", justify="center")
        table_2.add_column("Color", justify="center")
        table_2.add_column("Score Text", justify="center")
        table_2.add_column("Score", justify="center")
        table_2.add_row(prefix,
                        PlayerView.display_player_details(player_2),
                        sep,
                        color_2_,
                        score_text,
                        score_2_display)

        return Group(table_1, table_vs, table_2)

    def display_round_details(self, rnd: Round) -> Panel:
        """
        Method that displays the round details.
        Args:
            rnd (Round): The round object.

        Returns:
            The round details in Rich format.
        """
        start = f"[dim grey58]{rnd.start_date} {rnd.start_time}[/dim grey58]" \
            if rnd.start_date and rnd.start_time else "Not started"
        end = f"[dim grey58]{rnd.end_date} {rnd.end_time}[/dim grey58]" \
            if rnd.end_date and rnd.end_time else "Not finished"

        prefix_dates = "[dim grey58] (from [/dim grey58]"
        sep = "[dim grey58] → [/dim grey58]"
        suffix_dates = "[dim grey58])[/dim grey58]"
        round_name = f"[bold bright_white]{rnd.round_name}[/bold bright_white]"

        round_str = f"{round_name}{prefix_dates}{start}{sep}{end}{suffix_dates}"

        if not rnd.matches:
            return Panel(
                f"[bright_white]- The {rnd.round_name} has no matches yet.[/bright_white]",
                border_style="black",
                box=box.MINIMAL,
                expand=False
            )

        table = Table(
            show_header=False,
            box=box.MINIMAL,
            expand=False,
            padding=(0, 1),
            border_style="black",
        )
        table.add_column("Match info", justify="left")

        header = f"[bold bright_white]- The {round_str} has {len(rnd.matches)} matches:[/bold bright_white]\n"
        table.add_row(header)

        for match in rnd.matches:
            table.add_row(self.display_match_details(match) if match is not None else "")

        return Panel(Group(table), box=box.MINIMAL, expand=False)

    def display_tournament_details(self, tournament: Tournament) -> Group:
        """
        Method that displays the tournament details.
        Args:
            tournament (Tournament): The tournament object.

        Returns:
            The tournament details in Rich format.
        """
        name = f"[bold cyan]{tournament.name.upper()}[/bold cyan]"
        place_dates = (
            f"[white]({tournament.place}, {tournament.start_date} → {tournament.end_date}, "
            f"currently in round {tournament.current_round} of {tournament.rounds_number} rounds, "
            f"description: {tournament.description})[/white]"
        )
        header = Panel(
            f"[cyan]├─   [/cyan]{name} {place_dates}",
            expand=False,
            border_style="cyan"
        )

        rounds_panels = []
        if tournament.rounds:
            rounds_title = Panel("[bright_white]ALL ROUNDS[/bright_white]", expand=False)
            rounds_panels.append(rounds_title)

            for rnd in tournament.rounds:
                rounds_panels.append(Panel(self.display_round_details(rnd), border_style="white", expand=False))

        return Group(header, *rounds_panels)

    @staticmethod
    def display_tournaments_submenu() -> None:
        """
        Method that displays the tournaments submenu.
        """
        console.print("[bold bright_blue]\n▶ TOURNAMENTS ◀\n[/bold bright_blue]")
        console.print("[bright_blue]▷▷ 1. Create a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Update a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Display a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 4. Display all the tournaments[/bright_blue]")
        console.print("[bright_blue]▷▷ 5. Go back to main menu\n[/bright_blue]")

    @staticmethod
    def display_update_tournament_menu() -> None:
        """
        Method that displays the tournament submenu.
        """
        console.print("[bold bright_blue]\n▶ UPDATE A TOURNAMENT ◀\n[/bold bright_blue]")
        console.print("[bright_blue]▷▷ 1. Display all tournaments[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Add scores to a tournament[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Go back to main menu\n[/bright_blue]")

    @staticmethod
    def prompt_for_tournaments_submenu() -> int:
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
    def prompt_for_updating_tournament_menu() -> int:
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
    def prompt_for_updating_tournament_scores_menu() -> int:
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
    def prompt_for_tournament_name() -> str:
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
    def prompt_for_tournament_place() -> str:
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
    def prompt_for_tournament_start_date() -> str:
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
    def prompt_for_tournament_end_date() -> str:
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
    def prompt_for_tournament_description() -> str:
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
    def prompt_for_tournament_players_number() -> str:
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
    def tournament_exists(name: str, tournaments: Iterable[Tournament]) -> bool:
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

    def prompt_for_selecting_tournament(self, tournaments: Iterable[Tournament]) -> str | None:
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
    def prompt_for_asking_to_continue_tournament_filling() -> bool:
        """
        Method that prompts the users if they want to continue tournament scores filling.
        Returns:
            A boolean. True if the users want to pursue, False otherwise.
        """
        while True:
            question = Prompt.ask("[bright_white]▶ Do you want to pursue the completion of the tournament ? "
                                  "(y/n) [/bright_white]").strip()

            if not question:
                console.print(MESSAGE["empty"])
                continue

            if question in ("y", "yes"):
                return True

            elif question in ("n", "no"):
                return False

            else:
                console.print("[bold bright_red]❌[/bold bright_red] [bright_red]You must enter 'y' or 'n'."
                              "[/bright_red]")

    @staticmethod
    def prompt_for_selecting_tournament_rounds_number():
        """
        Method that prompts the users to choose the tournament rounds number.
        Returns:
            The rounds number in integer format.
        """
        while True:
            number = Prompt.ask("[bright_white]▶ Select the number of rounds [/bright_white]").strip()
            if number.isalpha():
                console.print(MESSAGE["alpha"])
                continue
            elif len(number) == 0:
                console.print(MESSAGE["empty"])
                continue
            elif not number.isalpha() and not number.isdigit():
                console.print(MESSAGE["invalid"])
                continue
            elif number.isdigit() and int(number) % 2 != 0:
                console.print(MESSAGE["not_even"])
                continue
            elif int(number) < 4:
                console.print(MESSAGE["digit_minimum"])
                continue
            return int(number)

    @staticmethod
    def display_tournament_name(tournament_name: str) -> None:
        """
        Method that displays the tournament name.
        Args:
            tournament_name (str): The tournament name.
        """
        console.print(tournament_name)

    def display_tournament(self, tournament: Tournament) -> None:
        """
        Method that displays a tournament object.
        """
        console.print(self.display_tournament_details(tournament))

    @staticmethod
    def display_setting_scores_title() -> None:
        """
        Method that displays the 'setting scores' title.
        """
        text = "⮞ Setting scores for current round :".upper()
        console.print(f"\n[bold bright_yellow]{text}[/bold bright_yellow]")

    def display_round(self, rnd: Round) -> None:
        """
        Method that displays a round object.
        Args:
            rnd (Round): The round object.
        """
        console.print(self.display_round_details(rnd))

    def display_tournaments(self, tournaments: Iterable[Tournament]) -> None:
        """
        Method that displays all the tournaments objects.
        Args:
            tournaments (Iterable[Tournament]): The tournaments object.
        """
        title = Panel(
            "[bold turquoise2]ALL TOURNAMENTS[/bold turquoise2]",
            border_style="bold turquoise2",
            expand=True
        )
        console.print(title)

        for tournament in tournaments:
            tournament_view = self.display_tournament_details(tournament)

            console.print(Panel(tournament_view, border_style="cyan", expand=True))

    @staticmethod
    def display_tournament_name_exists() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]The tournament's name already exists. "
                      "Please choose another one.\n[/bright_red]")

    @staticmethod
    def display_tournament_exists() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Tournament already in the database !\n"
                      "[/bright_red]")

    def display_tournament_added(self, current_tournament: Tournament) -> None:
        console.print("[bright_yellow]✅ New tournament added to database ![/bright_yellow]")
        console.print(self.display_tournament_details(current_tournament))

    def display_tournament_updated(self, current_tournament: Tournament) -> None:
        console.print("[bright_yellow]✅ Tournament updated in database ![/bright_yellow]")
        console.print(self.display_tournament_details(current_tournament))

    @staticmethod
    def display_all_tournaments_completed() -> None:
        console.print("[bright_red]⛔ All tournaments are completed. You can not add any score.\n[/bright_red]")

    @staticmethod
    def display_tournament_completed() -> None:
        console.print("[bright_red]Tournament already completed ! Please choose another one.\n[/bright_red]")

    @staticmethod
    def display_selected_tournament(tournament_name: str) -> None:
        console.print(f"[bright_yellow]\nSelected tournament: [/bright_yellow]{tournament_name}.")

    @staticmethod
    def display_tournament_round_score_saved(round_name: int) -> None:
        console.print(f"[bright_green]\nScores saved for[/bright_green] {round_name}.")

    @staticmethod
    def display_player_not_found() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Player not found. Please try again.\n"
                      "[/bright_red]")

    @staticmethod
    def display_player_exists() -> None:
        console.print("[bright_white]⚠️ Player already selected. Please choose another one.[/bright_white]\n")

    @staticmethod
    def display_player(player) -> str:
        """
        Method that displays the player's details.
        Args:
            player (Player): The player object.

        Returns:
            The details of the player.
        """
        str_id = f"[bold red]{player.identifier}[/bold red]"
        sep = "[grey53] - [/grey53]"
        str_name = f"[bold blue]{player.first_name} {player.name.upper()} [/bold blue]"
        str_date = f"[grey53]born on {player.birth_date}[/grey53]"
        return str_id + sep + str_name + str_date

    def display_player_added(self, player: Player, current_number: int, number: int) -> None:
        console.print(self.display_player(player))
        console.print(f"✅ [bright_yellow]added to tournament. ({current_number}/{number}).\n[/bright_yellow]")

    @staticmethod
    def display_no_scores_found() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]No players/scores found.[/bright_red]")

    @staticmethod
    def display_scores_bug() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Scores bug ![/bright_red]")

    @staticmethod
    def display_file_not_found(file_path: Path) -> None:
        console.print(f"[bright_white]{file_path} : [/bright_white][bright_red]❌ file not found ![/bright_red]\n")

    @staticmethod
    def display_winners(winners: list[Player], max_score: float, tournament_name: str) -> None:
        """
        Method that displays the tournament's winner(s).
        Args:
            winners (list[Player]): The winners of the tournament.
            max_score (float): The maximum score.
            tournament_name (str): The name of the tournament.
        """
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
    def display_player_details(player) -> str:
        """
        Method that displays the player's details.
        Args:
            player (Player): The player object.

        Returns:
            The details of the player.
        """
        str_id = f"[bold red]{player.identifier}[/bold red]"
        sep = "[grey53] - [/grey53]"
        str_name = f"[bold blue]{player.first_name} {player.name.upper()} [/bold blue]"
        str_date = f"[grey53]born on {player.birth_date}[/grey53]"
        return str_id + sep + str_name + str_date

    @staticmethod
    def display_players_submenu() -> None:
        """
        Method that displays the players submenu.
        """
        console.print("[bold bright_blue]\n▶ PLAYERS ◀\n[/bold bright_blue]")
        console.print("[bright_blue]▷▷ 1. Add a player into database[/bright_blue]")
        console.print("[bright_blue]▷▷ 2. Display the club players[/bright_blue]")
        console.print("[bright_blue]▷▷ 3. Go back to main menu\n[/bright_blue]")

    @staticmethod
    def display_enough_players() -> None:
        """
        Method that displays a 'not enough players' message.
        """
        console.print("\n[bright_red]There is not enough players to create a tournament.[/bright_red]\n")

    @staticmethod
    def display_no_players() -> None:
        """
        Method that displays a 'no players' message.
        """
        console.print("\n[bright_red]No players found. You can not create a new tournament before adding new players."
                      "[/bright_red]\n")

    @staticmethod
    def prompt_for_players_submenu() -> int | None:
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
    def prompt_for_player_name() -> str | None:
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
    def prompt_for_player_first_name() -> str | None:
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
    def prompt_for_player_birth_date() -> str | None:
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
    def prompt_for_player_identifier() -> str | None:
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
    def display_players(players: Iterable[Player]) -> None:
        """
        Method that displays the players list.
        Args:
            players (Iterable[Player]): The players list.
        """
        header = Panel(
            "ALL PLAYERS",
            border_style="bright_red",
            style="bright_red",
            expand=False
        )

        table = Table(
            show_header=False,
            header_style="bright_red",
            border_style="bright_red",
            expand=False
        )
        table.add_column("Identifier", justify="left", style="bold red")

        for player in players:
            str_id = f"[bold red]{player.identifier}[/bold red]"
            sep = "[grey53] - [/grey53]"
            str_name = f"[bold blue]{player.first_name} {player.name.upper()}[/bold blue]"
            str_date = f"[grey53]born on {player.birth_date}[/grey53]"
            table.add_row(f"{str_id}{sep}{str_name} {str_date}")

        group = Group(header, table)
        console.print(group)

    @staticmethod
    def player_exists(identifier: str, players: Iterable[Player]) -> bool:
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

    def prompt_for_selecting_players(self, all_players: Iterable[Player], numbers_left: int,
                                     selected_players: Iterable[Player]) -> None:
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

        self.display_players(all_players)

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

    def prompt_for_adding_player_score(self, player: Player) -> float | None:
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
    def display_player_identifier_exists() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]This identifier already assigned in database "
                      "![/bright_red]\n")

    @staticmethod
    def display_player_exists() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]This player already exists in database !"
                      "[/bright_red]\n")

    def display_player_added(self, player: Player) -> None:
        console.print("[bright_green]✅ New player added to database ![/bright_green]\n")
        console.print(self.display_player_details(player))

    @staticmethod
    def display_file_not_found(file_path: Path) -> None:
        console.print(f"[bright_white]{file_path} : [/bright_white][bright_red]❌ file not found ![/bright_red]\n")


class ReportView:

    @staticmethod
    def display_reports_menu() -> None:
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
    def prompt_for_reports_menu() -> int | None:
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
    def prompt_for_generating_report() -> str:
        """
        Method that prompts the user to choose to generate a report.
        Returns:
            The answer.
        """
        answer = Prompt.ask("\n[bright_white]▶ Do you want to generate the HTML report ? (y/n) [/bright_white]")
        return answer

    @staticmethod
    def display_file_not_found(path: Path) -> None:
        console.print(f"{path} : [bold bright_red]❌[/bold bright_red] [bright_red]file not found ![/bright_red]")

    @staticmethod
    def display_report_generated(path: Path) -> None:
        console.print(f"[bright_white]The HTML report has been generated.\nHere ⯈[/bright_white] {path}\n")

    @staticmethod
    def display_cancelled() -> None:
        console.print("[bright_white]Ok, cancelled.[/bright_white]")

    @staticmethod
    def display_yes_no() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]You must answer yes or no (y/n)."
                      "[/bright_red]")

    @staticmethod
    def display_sorted_players(number: int, players: Iterable[Player]) -> None:
        """
        Method that displays the players sorted.
        Args:
            number (int): The number of players sorted.
            players (Iterable[Player]): The sorted players list.
        """
        console.print(f"\n{number} [bright_white]players alphabetically sorted.[/bright_white]\n")
        PlayerView.display_players(players)
        console.print("\n")

    @staticmethod
    def display_sorted_tournaments(tournaments: Iterable[Tournament], tournament_view: TournamentView) -> None:
        """
        Method that displays the tournaments sorted.
        Args:
            tournaments (Iterable[Tournament]): The tournaments list.
            tournament_view (TournamentView): The tournament view.
        """
        console.print("\n[bright_white]The sorted tournaments.[/bright_white]\n")
        tournament_view.display_tournaments(tournaments)
        console.print("\n")

    @staticmethod
    def display_selected_tournament_title(tournament_name: str) -> None:
        console.print(f"\n[bright_white]The selected tournament[/bright_white] \"{tournament_name}\":\n")

    @staticmethod
    def display_rnd(rnd: Round, tournament_view: TournamentView) -> None:
        """
        Method that displays the round.
        Args:
            rnd (Round): The round object.
            tournament_view (TournamentView): The tournament view.
        """
        details = tournament_view.display_round_details(rnd)
        console.print(details)

    @staticmethod
    def display_all_rounds_and_matches_title(tournament_name: str) -> None:
        console.print(f"\n[bright_white]All the rounds and matches of selected tournament[/bright_white] "
                      f"\"{tournament_name}\":\n")

    @staticmethod
    def display_invalid_report_number() -> None:
        console.print("[bold bright_red]❌[/bold bright_red] [bright_red]Invalid report number.[/bright_red]")
