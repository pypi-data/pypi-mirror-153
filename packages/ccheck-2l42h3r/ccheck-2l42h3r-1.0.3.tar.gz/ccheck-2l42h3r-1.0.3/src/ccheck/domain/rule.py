"""Rule dataclass module"""

from typing import Pattern
from dataclasses import dataclass

from ccheck.domain.token.token_type import TokenType


@dataclass(slots=True)
class Rule:
    """Rule dataclass"""

    regex: Pattern[str]
    type: TokenType
