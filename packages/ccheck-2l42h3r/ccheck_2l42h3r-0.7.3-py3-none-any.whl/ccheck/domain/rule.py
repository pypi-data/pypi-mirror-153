from typing import Pattern
from dataclasses import dataclass

from ccheck.domain.token_type import TokenType


@dataclass
class Rule:
    regex: Pattern[str]
    type: TokenType
