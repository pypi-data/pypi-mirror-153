from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.for_loop import ForLoopExercise


class ForLoopExerciseCreator(ExerciseCreator):
    def factory_method(self) -> ForLoopExercise:
        return ForLoopExercise()
