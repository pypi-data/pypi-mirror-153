from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.variable_declaration import VariableDeclarationExercise


class VariableDeclarationExerciseCreator(ExerciseCreator):
    def factory_method(self) -> VariableDeclarationExercise:
        return VariableDeclarationExercise()
