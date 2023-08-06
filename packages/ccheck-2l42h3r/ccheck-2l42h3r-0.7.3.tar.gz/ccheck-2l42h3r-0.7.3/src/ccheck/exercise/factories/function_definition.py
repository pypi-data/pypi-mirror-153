from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.function_definition import FunctionDefinitionExercise


class FunctionDefinitionExerciseCreator(ExerciseCreator):
    def factory_method(self) -> FunctionDefinitionExercise:
        return FunctionDefinitionExercise()
