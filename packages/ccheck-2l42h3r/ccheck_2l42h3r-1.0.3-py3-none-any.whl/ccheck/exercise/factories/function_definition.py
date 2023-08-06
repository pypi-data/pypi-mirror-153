"""FunctionDefinitionExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.function_definition import FunctionDefinitionExercise


class FunctionDefinitionExerciseCreator(ExerciseCreator):
    """FunctionDefinitionExercise factory"""

    def factory_method(self) -> Exercise:
        return FunctionDefinitionExercise()
