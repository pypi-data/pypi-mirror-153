"""Token dataclass module"""

from dataclasses import dataclass
from typing import Any

from ccheck.domain.token.token_type import TokenType


@dataclass(slots=True)
class Token:
    """Token dataclass"""

    type: TokenType
    content: str

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Token):
            return self.type == other.type and self.content == other.content
        return False
