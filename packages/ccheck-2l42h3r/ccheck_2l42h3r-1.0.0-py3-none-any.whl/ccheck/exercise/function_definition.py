from typing import List

from ccheck.domain.validation_error import ValidationError
from ccheck.domain.token import Token
from ccheck.domain.exercise.exercise import Exercise


class FunctionDefinitionExercise(Exercise):
    def generate(self) -> str:
        return ""

    def validate(self, tokens: List[Token]) -> List[ValidationError]:
        return []
