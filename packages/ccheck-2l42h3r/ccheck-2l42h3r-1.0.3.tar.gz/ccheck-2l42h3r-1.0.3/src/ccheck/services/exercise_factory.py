"""ExerciseFactoryService class module"""

from typing import List
from ccheck.domain.exercise.exercise_type import ExerciseType
from ccheck.domain.exercise.exercise import Exercise
from ccheck.config import Config


class ExerciseFactoryService:
    """ExerciseFactoryService class"""

    __factory_list: List[Config.ExerciseFactoryDict]

    def __init__(self, config: Config) -> None:
        self.__factory_list = config.exercise_factories

    def create_exercise(self, exercise_type: ExerciseType) -> Exercise:
        """Return new constructed Exercise instance of given type"""
        for factory_dict in self.__factory_list:
            if factory_dict["exercise"].value == exercise_type.value:
                return factory_dict["factory"].factory_method()

        raise NotImplementedError
