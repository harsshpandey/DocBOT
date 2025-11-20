"""
Logging configuration for DocBot.
"""
import logging
import os
from utils.config import settings


def setup_logger(name: str = "docbot") -> logging.Logger:
    """Configure logging with both file and console handlers."""

    os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.log_level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(settings.log_file)
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()

