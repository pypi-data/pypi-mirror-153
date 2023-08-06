"""ForLoopExercise class module"""

import random
from ccheck.domain.token.token_type import TokenType

from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise


class ForLoopExercise(Exercise):
    """ForLoopExercise class"""

    def __init__(self) -> None:
        super().__init__()
        self.__generate()
        self.__create_validations()

    __iterations: int = 0

    def __generate(self) -> None:
        self.__iterations = random.randrange(3, 20)

    def get_description(self) -> str:
        return (
            "Zdefiniuj pętlę for, która wykona się "
            + str(self.__iterations)
            + " razy. "
            + "Niech zmienna kontrolna nazywa się 'i', "
            + "będzie typu 'int' i na początku ma wartość 0."
        )

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "for"),
                    Token(TokenType.OPEN_PAREN, "("),
                ],
                "Błędny zapis pętli for!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "int"),
                    Token(TokenType.IDENTIFIER, "i"),
                    Token(TokenType.OPERATOR, "="),
                    Token(TokenType.NUMBER, "0"),
                    Token(TokenType.OPERATOR, ";"),
                ],
                "Błędna deklaracja zmiennej kontrolnej!",
            )
        )
        self._add_validation(
            self._alternating_validation_builder(
                [
                    [
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, "<"),
                        Token(TokenType.NUMBER, str(self.__iterations)),
                        Token(TokenType.OPERATOR, ";"),
                    ],
                    [
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, "<"),
                        Token(TokenType.OPERATOR, "="),
                        Token(TokenType.NUMBER, str(self.__iterations - 1)),
                        Token(TokenType.OPERATOR, ";"),
                    ],
                    [
                        Token(TokenType.NUMBER, str(self.__iterations)),
                        Token(TokenType.OPERATOR, ">"),
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, ";"),
                    ],
                    [
                        Token(TokenType.NUMBER, str(self.__iterations - 1)),
                        Token(TokenType.OPERATOR, ">"),
                        Token(TokenType.OPERATOR, "="),
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, ";"),
                    ],
                ],
                "Błędny warunek zatrzymania pętli!",
            )
        )
        self._add_validation(
            self._alternating_validation_builder(
                [
                    [Token(TokenType.OPERATOR, "++"), Token(TokenType.IDENTIFIER, "i")],
                    [Token(TokenType.IDENTIFIER, "i"), Token(TokenType.OPERATOR, "++")],
                ],
                "Błędne wyrażenie iteracyjne!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")")],
                "Brak zakończenia zapisu pętli for!",
            )
        )
