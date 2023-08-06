"""VLADeclarationExercise class module"""

import secrets
from typing import List

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.token.token_type import TokenType


class VLADeclarationExercise(Exercise):
    """VLADeclarationExercise class"""

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
        self.__picked_length = secrets.randbelow(11) + 5
        self.__picked_type = secrets.choice(self.__variable_types)

    def get_description(self) -> str:
        return (
            "Zdefiniuj tablicę dynamiczną o nazwie "
            + self.__array_name
            + " za pomocą wskaźnika do pierwszego elementu tej tablicy "
            + "oraz funkcji 'malloc' oraz 'sizeof'. "
            + "Tablica powinna mieć rozmiar "
            + str(self.__picked_length)
            + " i przechowywać dane typu "
            + self.__picked_type
            + "."
        )

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, self.__picked_type),
                    Token(TokenType.OPERATOR, "*"),
                ],
                "Niepoprawny typ tablicy!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, self.__array_name)],
                "Niepoprawna nazwa tablicy!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.OPERATOR, "="),
                    Token(TokenType.IDENTIFIER, "malloc"),
                    Token(TokenType.OPEN_PAREN, "("),
                ],
                "Niepoprawna rezerwacja pamięci dla tablicy!",
            )
        )
        self._add_validation(
            self._alternating_validation_builder(
                [
                    [
                        Token(TokenType.NUMBER, str(self.__picked_length)),
                        Token(TokenType.OPERATOR, "*"),
                        Token(TokenType.IDENTIFIER, "sizeof"),
                        Token(TokenType.OPEN_PAREN, "("),
                        Token(TokenType.IDENTIFIER, self.__picked_type),
                        Token(TokenType.CLOSE_PAREN, ")"),
                    ],
                    [
                        Token(TokenType.IDENTIFIER, "sizeof"),
                        Token(TokenType.OPEN_PAREN, "("),
                        Token(TokenType.IDENTIFIER, self.__picked_type),
                        Token(TokenType.CLOSE_PAREN, ")"),
                        Token(TokenType.OPERATOR, "*"),
                        Token(TokenType.NUMBER, str(self.__picked_length)),
                    ],
                ],
                "Niepoprawne przeliczenie koniecznej pamięci dla tablicy!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.CLOSE_PAREN, ")"),
                    Token(TokenType.OPERATOR, ";"),
                ],
                "Brak zamknięcia nawiasu lub średnika na końcu linii!",
            )
        )
