"""Module contains common logger for seabattle app."""
import logging
import os
import uuid
from uuid import UUID

env_conf = os.environ.get("SEABATTLE_SETTINGS", "DevConfig")


def get_logger(game_id: UUID = uuid.uuid4(), name: str = "seabattle_default") -> logging.Logger:
    """
    Method defines common logger.
    Args:
        game_id: Game ID for logging.
        name: Logger name.

    Returns:
        logging.Logger: Logger object.
    """

    # Create logger object.
    logger_obj = logging.getLogger(str(game_id))

    # Define logger level.
    logger_obj.setLevel(logging.DEBUG if env_conf == "DevConfig" else logging.INFO)

    # Set up logger format and add handler to logger.
    log_format = f"%(asctime)s [%(threadName)-10s] [app: {name}, gameID: {game_id}] " \
                 "%(levelname)-8s - %(filename)s - %(funcName)s - line %(lineno)d - %(message)s"
    handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger_obj.addHandler(handler)

    return logger_obj


API_LOGGER = get_logger(name="seabattle_api")
