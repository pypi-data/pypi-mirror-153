from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.do_while_loop import DoWhileLoopExercise


class DoWhileLoopExerciseCreator(ExerciseCreator):
    def factory_method(self) -> DoWhileLoopExercise:
        return DoWhileLoopExercise()
