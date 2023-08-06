from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.vla_declaration import VLADeclarationExercise


class VLADeclarationExerciseCreator(ExerciseCreator):
    def factory_method(self) -> VLADeclarationExercise:
        return VLADeclarationExercise()
