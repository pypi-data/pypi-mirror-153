"""ValidationError dataclass module"""
from dataclasses import dataclass


@dataclass(slots=True)
class ValidationError:
    """ValidationError dataclass"""

    error_message: str
