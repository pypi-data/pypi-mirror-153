"""DoWhileLoopExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.do_while_loop import DoWhileLoopExercise


class DoWhileLoopExerciseCreator(ExerciseCreator):
    """DoWhileLoopExercise factory"""

    def factory_method(self) -> Exercise:
        return DoWhileLoopExercise()
