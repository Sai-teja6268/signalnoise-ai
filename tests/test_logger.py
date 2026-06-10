from signalnoise.observability.logger import (
    logger
)


def test_logger():

    logger.info(
        "Logger test"
    )

    assert True
