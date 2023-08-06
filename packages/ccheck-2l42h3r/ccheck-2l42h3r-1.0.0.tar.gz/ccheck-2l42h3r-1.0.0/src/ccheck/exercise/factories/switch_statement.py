from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.switch_statement import SwitchStatementExercise


class SwitchStatementExerciseCreator(ExerciseCreator):
    def factory_method(self) -> SwitchStatementExercise:
        return SwitchStatementExercise()
