"""Exercise types enum module"""

from enum import Enum


class ExerciseType(Enum):
    """Exercise types enum"""

    VARIABLE_DECLARATION = 1
    IF_STATEMENT = 2
    SWITCH_STATEMENT = 3
    FOR_LOOP_STATEMENT = 4
    DO_WHILE_LOOP_STATEMENT = 5
    STATIC_ARRAY_DECLARATION = 6
    VLA_POINTER_DECLARATION = 7
    FUNCTION_DEFINITION = 8
