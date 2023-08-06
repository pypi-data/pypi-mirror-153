"""ForLoopExercise factory module"""

from ccheck.domain.exercise.exercise import Exercise
from ccheck.domain.exercise.exercise_creator import ExerciseCreator
from ccheck.exercise.for_loop import ForLoopExercise


class ForLoopExerciseCreator(ExerciseCreator):
    """ForLoopExercise factory"""

    def factory_method(self) -> Exercise:
        return ForLoopExercise()
