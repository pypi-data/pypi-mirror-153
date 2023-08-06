"""Base Exercise class module"""

from abc import ABC, abstractmethod
from typing import List, Callable

from ccheck.domain.token.token import Token
from ccheck.domain.validation_error import ValidationError
from ccheck.utils.arrays import filter_out_none
from ccheck.utils.validation import (
    Validation,
    create_alternating_validation_builder,
    create_simple_validation_builder,
)


class Exercise(ABC):
    """Base Exercise class"""

    _validated: List[Token] = []
    __validations: List[Validation] = []

    _simple_validation_builder: Callable[[List[Token], str], Validation]

    _alternating_validation_builder: Callable[[List[List[Token]], str], Validation]

    def __init__(self) -> None:
        self._simple_validation_builder = create_simple_validation_builder(
            self._get_validated, self._set_validated
        )
        self._alternating_validation_builder = create_alternating_validation_builder(
            self._get_validated, self._set_validated
        )

    def _add_validation(self, validation: Validation) -> None:
        self.__validations.append(validation)

    def _get_validated(self) -> List[Token]:
        return self._validated

    def _set_validated(self, tokens: List[Token]) -> None:
        self._validated = self._validated + tokens

    @abstractmethod
    def get_description(self) -> str:
        """Return exercise description and guidelines"""

    def validate(self, tokens: List[Token]) -> List[ValidationError]:
        """Return array of errors from validating exercise input"""
        self._validated = []
        return filter_out_none(list(map(lambda v: v(tokens), self.__validations)))
