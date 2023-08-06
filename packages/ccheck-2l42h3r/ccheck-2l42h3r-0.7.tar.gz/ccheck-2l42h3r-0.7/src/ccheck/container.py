from dependency_injector import containers, providers

from ccheck.config import Config
from ccheck.services.application import ApplicationService
from ccheck.services.exercise_factory import ExerciseFactoryService
from ccheck.services.input import InputService
from ccheck.services.shell import ShellService
from ccheck.services.tokenizer import TokenizerService


class Container(containers.DeclarativeContainer):
    config = providers.Factory(Config)

    input_service = providers.Singleton(InputService)

    shell_service = providers.Singleton(
        ShellService, config=config, input_service=input_service
    )

    tokenizer_service = providers.Factory(TokenizerService, config=config)

    exercise_factory_service = providers.Factory(ExerciseFactoryService, config=config)

    application_service = providers.Singleton(
        ApplicationService,
        shell_service=shell_service,
        exercise_factory_service=exercise_factory_service,
        tokenizer_service=tokenizer_service,
    )
