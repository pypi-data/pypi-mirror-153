"""IfStatementExercise class module"""

import secrets
import string
from typing import Literal
from ccheck.domain.token.token_type import TokenType

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise


class IfStatementExercise(Exercise):
    """IfStatementExercise class"""

    def __init__(self) -> None:
        super().__init__()
        self.__generate()
        self.__create_validations()

    __variable_one: str
    __variable_two: str
    __condition: Literal["gt", "lt"]

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "if"), Token(TokenType.OPEN_PAREN, "(")],
                "Błędnie zapisana konstrukcja if!",
            )
        )
        self._add_validation(
            self._alternating_validation_builder(
                [
                    [
                        Token(TokenType.IDENTIFIER, self.__variable_one),
                        self.__get_valid_comparison_operator_token(),
                        Token(TokenType.IDENTIFIER, self.__variable_two),
                    ],
                    [
                        Token(TokenType.IDENTIFIER, self.__variable_two),
                        self.__get_valid_reverse_comparison_operator_token(),
                        Token(TokenType.IDENTIFIER, self.__variable_one),
                    ],
                ],
                "Błędnie zapisany warunek!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")")],
                "Błędnie zapisana konstrukcja if! (brak zamknięcia nawiasu)",
            )
        )

    def __generate(self) -> None:
        self.__variable_one = secrets.choice(string.ascii_lowercase)
        self.__variable_two = secrets.choice(string.ascii_lowercase)
        self.__condition = secrets.choice(["gt", "lt"])

    def get_description(self) -> str:
        return (
            "Zapisz jednolinijkową instrukcję warunkową if, w której sprawdzisz, czy zmienna '"
            + self.__variable_one
            + "' jest "
            + ("większa" if self.__condition == "gt" else "mniejsza")
            + " od zmiennej '"
            + self.__variable_two
            + "'."
        )

    def __get_valid_comparison_operator_token(self) -> Token:
        return Token(TokenType.OPERATOR, (">" if self.__condition == "gt" else "<"))

    def __get_valid_reverse_comparison_operator_token(self) -> Token:
        return Token(TokenType.OPERATOR, ("<" if self.__condition == "gt" else ">"))
