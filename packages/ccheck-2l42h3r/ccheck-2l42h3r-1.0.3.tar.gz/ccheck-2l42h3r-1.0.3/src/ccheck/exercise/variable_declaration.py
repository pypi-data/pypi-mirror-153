"""VariableDeclarationExercise class module"""

import secrets
from typing import List
from ccheck.domain.token.token_type import TokenType

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise


class VariableDeclarationExercise(Exercise):
    """VariableDeclarationExercise class"""

    __variable_types: List[str] = [
        "char",
        "unsigned char",
        "short",
        "unsigned short",
        "int",
        "unsigned int",
        "long",
        "unsigned long",
        "float",
        "double",
        "long double",
    ]
    __variable_name = "var"

    __picked_variable_type: str

    def __init__(self) -> None:
        super().__init__()
        self.__generate()
        self.__create_validations()

    def __generate(self) -> None:
        self.__picked_variable_type = secrets.choice(self.__variable_types)

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                self.__create_tokens_from_variable_type(), "Źle określony typ zmiennej!"
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, self.__variable_name)],
                "Błędna nazwa zmiennej!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.OPERATOR, ";")], "Brak średnika na końcu linii!"
            )
        )

    def get_description(self) -> str:
        return (
            'Zdefiniuj zmienną o nazwie "'
            + self.__variable_name
            + '" typu '
            + self.__picked_variable_type
            + ". Nie inicjalizuj zmiennej."
        )

    def __create_tokens_from_variable_type(self) -> List[Token]:
        return list(
            map(
                lambda word: Token(TokenType.IDENTIFIER, word),
                self.__picked_variable_type.split(),
            )
        )
