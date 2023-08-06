"""Main application module"""

from dependency_injector.wiring import Provide, inject

from ccheck.container import Container
from ccheck.services.application import ApplicationService


@inject
def main(
    application_service: ApplicationService = Provide[Container.application_service],
) -> None:
    """Application entrypoint"""
    application_service.run()


if __name__ == "__main__":
    container = Container()
    container.init_resources()  # type: ignore
    container.wire(modules=[__name__])

    main()
