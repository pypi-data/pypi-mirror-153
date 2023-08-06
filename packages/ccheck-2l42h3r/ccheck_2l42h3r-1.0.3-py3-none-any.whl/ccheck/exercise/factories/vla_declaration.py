"""VLADeclarationExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.vla_declaration import VLADeclarationExercise


class VLADeclarationExerciseCreator(ExerciseCreator):
    """VLADeclarationExercise factory"""

    def factory_method(self) -> Exercise:
        return VLADeclarationExercise()
