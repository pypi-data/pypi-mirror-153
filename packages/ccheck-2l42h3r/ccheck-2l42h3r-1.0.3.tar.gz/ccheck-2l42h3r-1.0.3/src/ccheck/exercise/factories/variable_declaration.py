"""VariableDeclarationExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.variable_declaration import VariableDeclarationExercise


class VariableDeclarationExerciseCreator(ExerciseCreator):
    """VariableDeclarationExercise factory"""

    def factory_method(self) -> Exercise:
        return VariableDeclarationExercise()
