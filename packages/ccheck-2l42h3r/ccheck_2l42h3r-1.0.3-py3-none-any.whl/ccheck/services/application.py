"""ApplicationService class module"""

import sys
from ccheck.domain.exercise.exercise_type import ExerciseType
from ccheck.services.exercise_factory import ExerciseFactoryService
from ccheck.domain.exercise.exercise import Exercise
from ccheck.services.shell import ShellService
from ccheck.services.tokenizer import TokenizerService
from ccheck.utils.validation import remove_whitespace_tokens


class ApplicationService:
    """ApplicationService class"""

    __shell_service: ShellService
    __exercise_factory_service: ExerciseFactoryService
    __tokenizer_service: TokenizerService
    __exercise: Exercise

    def __init__(
        self,
        shell_service: ShellService,
        exercise_factory_service: ExerciseFactoryService,
        tokenizer_service: TokenizerService,
    ) -> None:
        self.__shell_service = shell_service
        self.__exercise_factory_service = exercise_factory_service
        self.__tokenizer_service = tokenizer_service

    def __on_exercise_select(self, exercise_type: ExerciseType) -> None:
        self.__exercise = self.__exercise_factory_service.create_exercise(exercise_type)
        ShellService.print_exercise_question(self.__exercise)

    def __exercise_runloop(self) -> None:
        while True:
            solution = self.__shell_service.read_solution()
            tokens_no_whitespace = remove_whitespace_tokens(
                self.__tokenizer_service.tokenize(solution)
            )
            errors = self.__exercise.validate(tokens_no_whitespace)
            if len(errors) == 0:
                self.__shell_service.print_success_message()
                break
            ShellService.print_error_message(errors[0])
            if not ShellService.ask_for_retry():
                break

    def run(self) -> None:
        """Read selected exercise and run answer-checking loop"""
        try:
            self.__shell_service.print_exercise_list(self.__on_exercise_select)
        except ValueError:
            print("Niepoprawny numer zadania!")
            sys.exit(1)

        self.__exercise_runloop()
