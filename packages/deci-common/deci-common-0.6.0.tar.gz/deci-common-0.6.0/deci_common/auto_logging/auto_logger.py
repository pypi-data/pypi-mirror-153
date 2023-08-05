import json
import os

import pkg_resources

from deci_common.environment.environment_config import DEFAULT_LOGGING_LEVEL


class AutoLoggerConfig:
    """
    A Class for the Automated Logging Config that is created from the JSON config file (auto_logging_conf)
    """

    @staticmethod
    def generate_config_for_module_name(
        module_name, log_level=DEFAULT_LOGGING_LEVEL, max_bytes=10485760, handlers_list=None
    ) -> dict:
        """
        generate_config_for_module_name - Returns a Config Dict For Logging
            :param module_name:     The Python Module name to create auto_logging for
            :param log_level:       Minimal log level to set for the new auto_logging
            :param max_bytes:       Max size for the log file before rotation starts
            :param handlers_list:    A list specifying the handlers (Console, etc..) - Better Leave Empty or None
            :return: python dict() with the new auto_logging for the module
        """

        # LOADING THE ORIGINAL ROOT CONFIG FILE
        conf_file_name = "auto_logging_conf.json"
        conf_file_path = os.path.join(pkg_resources.resource_filename("deci_common", "/auto_logging/"), conf_file_name)

        with open(conf_file_path, "r") as logging_configuration_file:
            config_dict = json.load(logging_configuration_file)

        if os.environ.get("JSON_LOG_FORMAT") is not None:
            config_dict["handlers"]["console"]["formatter"] = "jsonFormatter"

        # CREATING THE PATH TO THE "HOME" FOLDER WITH THE LOG FILE NAME
        log_file_name = module_name + ".log"
        user_dir = os.path.expanduser(r"~")
        logs_dir_path = os.path.join(user_dir, "deci_logs")

        if not os.path.exists(logs_dir_path):
            try:
                os.mkdir(logs_dir_path)
            except Exception as ex:
                print(
                    "[WARNING] - deci_logs folder was not found and couldn't be created from the code - "
                    "All of the Log output will be sent to Console!" + str(ex)
                )

            # CREATING ONLY A CONSOLE LOG HANDLER
            handlers_list = ["console"]
            logger = {"level": log_level, "handlers": handlers_list, "propagate": False}
            config_dict["loggers"][module_name] = logger

            return config_dict

        log_file_path = os.path.join(logs_dir_path, log_file_name)

        # THE ENTRIES TO ADD TO THE ORIGINAL CONFIGURATION
        handler_name = module_name + "_file_handler"
        file_handler = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": log_level,
            "formatter": "fileFormatter",
            "filename": log_file_path,
            "maxBytes": max_bytes,
            "backupCount": 20,
            "encoding": "utf8",
        }

        # CREATING MULTIPLE HANDLERS - A LOGGING FILE HANDLER AND A CONSOLE HANDLER
        if handlers_list is None or handlers_list.empty():
            handlers_list = ["console", handler_name]

        logger = {"level": log_level, "handlers": handlers_list, "propagate": False}

        # ADDING THE NEW LOGGER ENTRIES TO THE CONFIG DICT
        config_dict["handlers"][handler_name] = file_handler
        config_dict["loggers"][module_name] = logger
        config_dict["root"]["handlers"].append(handler_name)

        return config_dict
