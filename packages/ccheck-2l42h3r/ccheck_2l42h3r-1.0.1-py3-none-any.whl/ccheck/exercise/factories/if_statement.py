from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.if_statement import IfStatementExercise


class IfStatementExerciseCreator(ExerciseCreator):
    def factory_method(self) -> IfStatementExercise:
        return IfStatementExercise()
