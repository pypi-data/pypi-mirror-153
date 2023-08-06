"""FunctionDefinitionExercise class module"""

import secrets
from typing import Dict, List, Literal

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.token.token_type import TokenType

OperationType = Literal["addition", "subtraction", "multiplication", "division"]


class FunctionDefinitionExercise(Exercise):
    """FunctionDefinitionExercise class"""

    __operation_types: List[OperationType] = [
        "addition",
        "subtraction",
        "multiplication",
        "division",
    ]

    __operator_switch: Dict[OperationType, str] = {
        "addition": "+",
        "subtraction": "-",
        "multiplication": "*",
        "division": "/",
    }

    __function_name_switch: Dict[OperationType, str] = {
        "addition": "suma",
        "subtraction": "odejmowanie",
        "multiplication": "mnozenie",
        "division": "dzielenie",
    }

    __picked_operation_type: OperationType

    def __init__(self) -> None:
        super().__init__()
        self.__generate()
        self.__create_validations()

    def __generate(self) -> None:
        self.__picked_operation_type = secrets.choice(self.__operation_types)

    def get_description(self) -> str:
        return (
            "Zapisz funkcję typu int o nazwie "
            + self.__function_name_switch.get(self.__picked_operation_type)  # type: ignore
            + ", która przyjmie argumenty a i b typu int, "
            + "po czym zwróci wynik żądanej operacji. Nie używaj zmiennych pomocniczych."
        )

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "int")],
                "Nieprawidłowy typ wartości zwracanej przez funkcję!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(
                        TokenType.IDENTIFIER,
                        self.__function_name_switch.get(self.__picked_operation_type),  # type: ignore
                    )
                ],
                "Nieprawidłowa nazwa funkcji!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.OPEN_PAREN, "(")],
                "Nieprawidłowy zapis struktury funkcji!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "int"),
                    Token(TokenType.IDENTIFIER, "a"),
                    Token(TokenType.OPERATOR, ","),
                    Token(TokenType.IDENTIFIER, "int"),
                    Token(TokenType.IDENTIFIER, "b"),
                ],
                "Nieprawidłowe argumenty funkcji!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")"), Token(TokenType.OPEN_CURLY, "{")],
                "Nieprawidłowy zapis struktury funkcji!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "return")],
                "Brak klauzuli 'return' w funkcji!",
            )
        )
        if self.__picked_operation_type in ("addition", "multiplication"):
            self._add_validation(
                self._alternating_validation_builder(
                    [
                        [
                            Token(TokenType.IDENTIFIER, "a"),
                            Token(
                                TokenType.OPERATOR,
                                self.__operator_switch.get(
                                    self.__picked_operation_type
                                ),  # type: ignore
                            ),
                            Token(TokenType.IDENTIFIER, "b"),
                        ],
                        [
                            Token(TokenType.IDENTIFIER, "b"),
                            Token(
                                TokenType.OPERATOR,
                                self.__operator_switch.get(
                                    self.__picked_operation_type
                                ),  # type: ignore
                            ),
                            Token(TokenType.IDENTIFIER, "a"),
                        ],
                    ],
                    "Błąd w zwracanym wyniku!",
                )
            )
        else:
            self._add_validation(
                self._simple_validation_builder(
                    [
                        Token(TokenType.IDENTIFIER, "a"),
                        Token(
                            TokenType.OPERATOR,
                            self.__operator_switch.get(
                                self.__picked_operation_type
                            ),  # type: ignore
                        ),
                        Token(TokenType.IDENTIFIER, "b"),
                    ],
                    "Błąd w zwracanym wyniku!",
                )
            )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.OPERATOR, ";")],
                "Błąd w zapisie klauzuli return funkcji (brak średnika na końcu linii)!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_CURLY, "}")],
                "Błąd w zapisie struktury funkcji (brak zamknięcia klamry)!",
            )
        )
