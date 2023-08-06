"""ShellService class module"""

from typing import List, Callable

from ccheck.config import Config
from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_type import ExerciseType
from ccheck.domain.validation_error import ValidationError
from ccheck.services.input import InputService


class ShellService:
    """ShellService class"""

    __exercise_list: List[Config.ExerciseDict]

    def __init__(self, config: Config) -> None:
        self.__exercise_list = config.exercise_config

    def __is_input_valid_exercise_number(self, typed: str) -> bool:
        try:
            val = int(typed)
            if val <= len(self.__exercise_list):
                return True
            return False
        except ValueError:
            return False

    def print_exercise_list(
        self, on_exercise_select: Callable[[ExerciseType], None]
    ) -> None:
        """Print available exercise list, execute callback on select"""
        print("Dostępne rodzaje zadań:")
        for index, exercise in enumerate(self.__exercise_list, start=1):
            print(index, ") ", exercise["name"])
        typed = input("Wybierz numer zadania: ")

        if self.__is_input_valid_exercise_number(typed):
            on_exercise_select(self.__exercise_list[int(typed) - 1]["exercise"])
        else:
            raise ValueError

    @staticmethod
    def print_exercise_question(exercise: Exercise) -> None:
        """Print selected exercise question"""
        print(exercise.get_description())

    @staticmethod
    def read_solution() -> str:
        """Print solution helper message and return read input"""
        print(
            "Wprowadź swoje rozwiązanie. "
            + "By zakończyć wciśnij Enter i Ctrl+D (Enter + Ctrl+Z + Enter na Windows). "
            + "Nie importuj bibliotek, wprowadzaj jedynie wymagany kod."
        )
        return InputService.get_multiline_input()

    @staticmethod
    def ask_for_retry() -> bool:
        """Ask whether to retry until given correct unswer"""
        while True:
            typed = input("Czy chcesz spróbować ponownie? [T/N]: ")
            if typed in ("Y", "y", "T", "t", "N", "n"):
                return typed in ("Y", "y", "T", "t")

    @staticmethod
    def print_success_message() -> None:
        """Prints correct answer message"""
        print("Poprawna odpowiedź!")

    @staticmethod
    def print_error_message(error: ValidationError) -> None:
        """Prints error message given an error"""
        print("Znaleziono błąd: " + error.error_message)
