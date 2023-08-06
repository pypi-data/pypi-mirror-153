"""StaticArrayDeclarationExercise class module"""

import secrets
from typing import List

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.token.token_type import TokenType


class StaticArrayDeclarationExercise(Exercise):
    """StaticArrayDeclarationExercise class"""

    __variable_types: List[str] = [
        "char",
        "short",
        "int",
        "long",
        "float",
        "double",
    ]
    __array_name = "arr"

    __picked_type: str
    __picked_length: int

    def __init__(self) -> None:
        super().__init__()
        self.__generate()
        self.__create_validations()

    def __generate(self) -> None:
        self.__picked_type = secrets.choice(self.__variable_types)
        self.__picked_length = secrets.randbelow(9) + 2

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, self.__picked_type)], "Błędny typ tablicy!"
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, self.__array_name)],
                "Błędna nazwa tablicy!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.OPEN_SQUARE, "[")], "Błędny zapis tablicy statycznej!"
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.NUMBER, str(self.__picked_length))],
                "Błędna długość tablicy!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.CLOSE_SQUARE, "]"),
                    Token(TokenType.OPERATOR, ";"),
                ],
                "Błędny zapis tablicy statycznej!",
            )
        )

    def get_description(self) -> str:
        return (
            "Zadeklaruj tablicę wartości typu "
            + self.__picked_type
            + " o stałej długości równej "
            + str(self.__picked_length)
            + " i nazwie '"
            + self.__array_name
            + "'. Nie inicjalizuj tablicy."
        )
