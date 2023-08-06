"""DoWhileLoopExercise class module"""

import random
from ccheck.domain.token.token_type import TokenType
from ccheck.domain.token.token import Token
from ccheck.domain.exercise.exercise import Exercise


class DoWhileLoopExercise(Exercise):
    """DoWhileLoopExercise class"""

    def __init__(self) -> None:
        super().__init__()
        self.__generate()
        self.__create_validations()

    __iterations: int = 0

    def __generate(self) -> None:
        self.__iterations = random.randrange(3, 20)

    def __create_validations(self) -> None:
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "int"),
                    Token(TokenType.IDENTIFIER, "i"),
                    Token(TokenType.OPERATOR, "="),
                    Token(TokenType.NUMBER, "0"),
                    Token(TokenType.OPERATOR, ";"),
                ],
                "Błąd w definicji zmiennej kontrolnej!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.IDENTIFIER, "do"), Token(TokenType.OPEN_CURLY, "{")],
                "Błąd w zapisie struktury do..while!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.IDENTIFIER, "test"),
                    Token(TokenType.OPEN_PAREN, "("),
                    Token(TokenType.IDENTIFIER, "i"),
                    Token(TokenType.CLOSE_PAREN, ")"),
                    Token(TokenType.OPERATOR, ";"),
                ],
                "Błąd w wyłowaniu efektu ubocznego pętli (funkcji 'test')!",
            )
        )
        self._add_validation(
            self._alternating_validation_builder(
                [
                    [
                        Token(TokenType.OPERATOR, "++"),
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, ";"),
                    ],
                    [
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, "++"),
                        Token(TokenType.OPERATOR, ";"),
                    ],
                ],
                "Błąd przy modyfikacji zmiennej kontrolnej!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [
                    Token(TokenType.CLOSE_CURLY, "}"),
                    Token(TokenType.IDENTIFIER, "while"),
                    Token(TokenType.OPEN_PAREN, "("),
                ],
                "Błąd na końcu zapisu struktury do..while!",
            )
        )
        self._add_validation(
            self._alternating_validation_builder(
                [
                    [
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, "<"),
                        Token(TokenType.NUMBER, str(self.__iterations)),
                    ],
                    [
                        Token(TokenType.IDENTIFIER, "i"),
                        Token(TokenType.OPERATOR, "<"),
                        Token(TokenType.OPERATOR, "="),
                        Token(TokenType.NUMBER, str(self.__iterations - 1)),
                    ],
                    [
                        Token(TokenType.NUMBER, str(self.__iterations)),
                        Token(TokenType.OPERATOR, ">"),
                        Token(TokenType.IDENTIFIER, "i"),
                    ],
                    [
                        Token(TokenType.NUMBER, str(self.__iterations - 1)),
                        Token(TokenType.OPERATOR, ">"),
                        Token(TokenType.OPERATOR, "="),
                        Token(TokenType.IDENTIFIER, "i"),
                    ],
                ],
                "Błędny warunek zatrzymania pętli!",
            )
        )
        self._add_validation(
            self._simple_validation_builder(
                [Token(TokenType.CLOSE_PAREN, ")"), Token(TokenType.OPERATOR, ";")],
                "Błąd na końcu zapisu struktury do..while! (Brak nawiasu lub średnika)",
            )
        )

    def get_description(self) -> str:
        return (
            "Zdefiniuj pętlę do..while, która wykona się "
            + str(self.__iterations)
            + " razy. "
            + "Zdefiniuj zmienną kontrolną 'i' typu 'int', która na początku ma wartość 0. "
            + "Dla każdego wykonania pętli wywołaj daną funkcję 'test', "
            + "która jako jedyny argument przyjmie obecną wartość zmiennej kontrolnej. "
            + "Zmianę wartości zmiennej kontrolnej przeprowadź dopiero po wywołaniu funkcji 'test'."
        )
