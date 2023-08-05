import os


class TerminalColours:
    """
    Usage: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python?page=1&tab=votes#tab-top
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class ColouredTextFormatter:
    @staticmethod
    def print_coloured_text(text: str, colour: str):
        """
        Prints a text with colour ascii characters.
        """
        return print("".join([colour, text, TerminalColours.ENDC]))


def get_environ_as_type(environment_variable_name: str, default=None, cast_to_type: type = str) -> object:
    """
    Tries to get an environment variable and cast it into a requested type.
    :return: cast_to_type object, or None if failed.
    :raises ValueError: If the value could not be casted into type 'cast_to_type'
    """
    value = os.environ.get(environment_variable_name, default)
    if value is not None:
        try:
            return cast_to_type(value)
        except Exception as e:
            print(e)
            raise ValueError(
                f"Failed to cast environment variable {environment_variable_name} to type {cast_to_type}: the value {value} is not a valid {cast_to_type}"
            )
    return
