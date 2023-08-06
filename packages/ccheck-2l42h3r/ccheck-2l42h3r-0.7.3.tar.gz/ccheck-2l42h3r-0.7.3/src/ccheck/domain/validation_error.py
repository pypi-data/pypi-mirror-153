from dataclasses import dataclass


@dataclass
class ValidationError:
    error_message: str
