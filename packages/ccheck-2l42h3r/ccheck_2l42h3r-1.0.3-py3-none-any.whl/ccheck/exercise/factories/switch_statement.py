"""SwitchStatementExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.switch_statement import SwitchStatementExercise


class SwitchStatementExerciseCreator(ExerciseCreator):
    """SwitchStatementExercise factory"""

    def factory_method(self) -> Exercise:
        return SwitchStatementExercise()
