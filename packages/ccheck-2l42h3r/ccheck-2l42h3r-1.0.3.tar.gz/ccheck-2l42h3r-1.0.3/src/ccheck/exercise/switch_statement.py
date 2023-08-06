"""SwitchStatementExercise class module"""

import secrets
from typing import List

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.token.token_type import TokenType
from ccheck.utils.validation import Validation


class SwitchStatementExercise(Exercise):
    """SwitchStatementExercise class"""

    __special_case: int

    def __init__(self) -> None:
        super().__init__()
        self.__generate()
        self.__create_validations()

    def __generate(self) -> None:
        self.__special_case = secrets.randbelow(10)

    def __create_break_validation(self) -> Validation:
        return self._simple_validation_builder(
            [Token(TokenType.IDENTIFIER, "break"), Token(TokenType.OPERATOR, ";")],
            "Brak instrukcji break!",
        )

    def __create_puts_call_validations(self, text: str) -> List[Validation]:
        return [
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "puts"), Token(TokenType.OPEN_PAREN, "(")],
                "Błędny zapis wyrażenia puts!",
            ),
            self._simple_validation_builder(
                [Token(TokenType.QUOTE, '"' + text + '"')],
                "Błędny zapis wyrażenia puts! (błąd w wypisywanej wartości)",
            ),
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")"), Token(TokenType.OPERATOR, ";")],
                "Błędny zapis wyrażenia puts!",
            ),
        ]

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "switch"),
                    Token(TokenType.OPEN_PAREN, "("),
                ],
                "Błędny zapis instrukcji switch-case!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "var")],
                "Błędne wyrażenie w instrukcji switch-case!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")"), Token(TokenType.OPEN_CURLY, "{")],
                "Błędny zapis instrukcji switch-case!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "case"),
                    Token(TokenType.NUMBER, str(self.__special_case)),
                    Token(TokenType.OPERATOR, ":"),
                ],
                "Błędny zapis szczególnego przypadku!",
            )
        )
        for validation in self.__create_puts_call_validations("znaleziono!"):
            self._add_validation(validation)
        self._add_validation(self.__create_break_validation())
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "default"),
                    Token(TokenType.OPERATOR, ":"),
                ],
                "Brak obsługi wypadku 'default'!",
            )
        )
        for validation in self.__create_puts_call_validations("brak"):
            self._add_validation(validation)
        self._add_validation(self.__create_break_validation())
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_CURLY, "}")],
                "Błędny zapis instrukcji switch-case! (brak zamknięcia klamry)",
            )
        )

    def get_description(self) -> str:
        return (
            "Zapisz konstrukcję warunkową switch-case, "
            + "która jako wyrażenie przyjmie zmienną 'var' (jej typ - 'int'). "
            + "W przypadku wystąpienia liczby "
            + str(self.__special_case)
            + ", wypisz tekst 'znaleziono!' używając instrukcji 'puts'. "
            + "W dowolnym innym wypadku wypisz 'brak'."
        )
