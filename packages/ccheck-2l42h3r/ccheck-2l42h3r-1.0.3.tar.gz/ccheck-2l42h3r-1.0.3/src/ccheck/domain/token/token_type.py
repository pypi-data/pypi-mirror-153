"""Token enum module"""

from enum import Enum, auto


class TokenType(Enum):
    """Token type enum"""

    WHITESPACE = auto()
    WORD = auto()
    NUMBER = auto()
    AREA_COMMENT = auto()
    AREA_COMMENT_CONTINUE = auto()
    LINE_COMMENT = auto()
    QUOTE = auto()
    CHAR = auto()
    CHAR_CONTINUE = auto()
    DIRECTIVE = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    OPEN_SQUARE = auto()
    CLOSE_SQUARE = auto()
    OPEN_CURLY = auto()
    CLOSE_CURLY = auto()
    OPERATOR = auto()
    IDENTIFIER = auto()
    LINE_CONTINUE = auto()
