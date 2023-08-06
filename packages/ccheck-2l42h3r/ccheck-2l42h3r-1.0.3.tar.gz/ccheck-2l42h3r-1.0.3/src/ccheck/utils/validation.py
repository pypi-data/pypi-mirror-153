"""Functions aiding validations"""

from typing import List, Callable, Optional

from ccheck.domain.token.token import Token
from ccheck.domain.token.token_type import TokenType
from ccheck.domain.validation_error import ValidationError
from ccheck.utils.arrays import check_for_ordered_subarray, flatten

Validation = Callable[[List[Token]], Optional[ValidationError]]


def remove_whitespace_tokens(array: List[Token]) -> List[Token]:
    """Remove all whitespace tokens (for checks where whitespaces do not matter)"""
    return list(filter(lambda t: t.type != TokenType.WHITESPACE, array.copy()))


def create_simple_validation_builder(
    validated_getter: Callable[[], List[Token]],
    validated_setter: Callable[[List[Token]], None],
) -> Callable[[List[Token], str], Validation]:
    """Bind exercise class validated getter and setter to simple validation builder"""

    def builder(
        tokens_to_find: List[Token], validation_error_message: str
    ) -> Validation:
        return build_simple_validation(
            tokens_to_find, validation_error_message, validated_getter, validated_setter
        )

    return builder


def create_alternating_validation_builder(
    validated_getter: Callable[[], List[Token]],
    validated_setter: Callable[[List[Token]], None],
) -> Callable[[List[List[Token]], str], Validation]:
    """Bind exercise class validated getter and setter to alternating validation builder"""

    def builder(
        tokens_variants: List[List[Token]], validation_error_message: str
    ) -> Validation:
        return build_alternating_validation(
            tokens_variants,
            validation_error_message,
            validated_getter,
            validated_setter,
        )

    return builder


def build_alternating_validation(
    tokens_variants: List[List[Token]],
    validation_error_message: str,
    validated_getter: Callable[[], List[Token]],
    validated_setter: Callable[[List[Token]], None],
) -> Validation:
    """Return new validation checking for tokens occouring in correct order"""

    def validation(all_tokens: List[Token]) -> Optional[ValidationError]:
        for token_possibility in tokens_variants:
            if check_for_ordered_subarray(
                all_tokens, flatten([validated_getter(), token_possibility])
            ):
                validated_setter(token_possibility)
                return None
        return ValidationError(validation_error_message)

    return validation


def build_simple_validation(
    tokens_to_find: List[Token],
    validation_error_message: str,
    validated_getter: Callable[[], List[Token]],
    validated_setter: Callable[[List[Token]], None],
) -> Validation:
    """
    Return new validation checking for multiple,
    mutually exclusive instances of tokens
    occouring in correct order
    """

    def validation(all_tokens: List[Token]) -> Optional[ValidationError]:
        if check_for_ordered_subarray(
            all_tokens, flatten([validated_getter(), tokens_to_find])
        ):
            validated_setter(tokens_to_find)
            return None
        return ValidationError(validation_error_message)

    return validation
