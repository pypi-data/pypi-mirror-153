from abc import ABC, abstractmethod

from ccheck.domain.exercise.exercise import Exercise


class ExerciseCreator(ABC):
    @abstractmethod
    def factory_method(self) -> Exercise:
        pass
