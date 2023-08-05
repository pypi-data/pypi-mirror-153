import logging
import logging.config

from deci_common.auto_logging import AutoLoggerConfig


def get_logger(logger_name: str) -> logging.Logger:
    config_dict = AutoLoggerConfig.generate_config_for_module_name(logger_name)
    logging.config.dictConfig(config_dict)
    logger: logging.Logger = logging.getLogger(logger_name)
    return logger


class ILogger:
    """
    Provides logging capabilities to the derived class.
    """

    def __init__(self, logger_name: str = None):
        logger_name = logger_name if logger_name else str(self.__module__)
        self._logger: logging.Logger = get_logger(logger_name)
