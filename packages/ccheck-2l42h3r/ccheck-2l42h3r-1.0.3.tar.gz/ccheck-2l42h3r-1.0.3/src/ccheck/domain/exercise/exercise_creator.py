"""Exercise factory interface module"""

from abc import ABC, abstractmethod

from ccheck.domain.exercise.exercise import Exercise


class ExerciseCreator(ABC):
    """Exercise factory interface"""

    @abstractmethod
    def factory_method(self) -> Exercise:
        """Exercise factory method"""
