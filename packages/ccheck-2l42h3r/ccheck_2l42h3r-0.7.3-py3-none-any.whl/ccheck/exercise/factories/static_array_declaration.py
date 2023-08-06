from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.static_array_declaration import StaticArrayDeclarationExercise


class StaticArrayExerciseCreator(ExerciseCreator):
    def factory_method(self) -> StaticArrayDeclarationExercise:
        return StaticArrayDeclarationExercise()
