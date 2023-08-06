"""IfStatementExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.if_statement import IfStatementExercise


class IfStatementExerciseCreator(ExerciseCreator):
    """IfStatementExercise factory"""

    def factory_method(self) -> Exercise:
        return IfStatementExercise()
