from typing import List, Callable

from ccheck.config import Config
from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_type import ExerciseType
from ccheck.domain.validation_error import ValidationError
from ccheck.services.input import InputService


class ShellService:
    __exercise_list: List[Config.ExerciseDict]
    __input_service: InputService

    def __init__(self, config: Config, input_service: InputService) -> None:
        self.__exercise_list = config.exercise_config
        self.__input_service = input_service

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
        print(exercise.get_description())

    def read_solution(self) -> str:
        print(
            "Wprowadź swoje rozwiązanie. By zakończyć wciśnij Enter i Ctrl+D (Ctrl+Z na Windows). Nie importuj bibliotek, wprowadzaj jedynie wymagany kod."
        )
        return self.__input_service.get_multiline_input()

    @staticmethod
    def ask_for_retry() -> bool:
        while True:
            typed = input("Czy chcesz spróbować ponownie? [T/N]: ")
            if typed in ("Y", "y", "T", "t", "N", "n"):
                return typed in ("Y", "y", "T", "t")

    @staticmethod
    def print_success_message() -> None:
        print("Poprawna odpowiedź!")

    @staticmethod
    def print_error_message(error: ValidationError) -> None:
        print("Znaleziono błąd: " + error.error_message)
