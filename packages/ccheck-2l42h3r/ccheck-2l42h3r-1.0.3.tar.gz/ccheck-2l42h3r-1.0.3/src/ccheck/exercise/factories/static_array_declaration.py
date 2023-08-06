"""StaticArrayExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.static_array_declaration import StaticArrayDeclarationExercise


class StaticArrayExerciseCreator(ExerciseCreator):
    """StaticArrayExercise factory"""

    def factory_method(self) -> Exercise:
        return StaticArrayDeclarationExercise()
