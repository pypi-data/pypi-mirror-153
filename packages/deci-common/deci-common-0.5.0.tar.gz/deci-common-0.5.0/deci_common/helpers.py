from uuid import uuid4
from enum import Enum
from typing import Type, List, Dict


def get_random_uuid_string() -> str:
    """
    Returns a uuid4 without dashes.
    """
    return str(uuid4()).replace("-", "")


def get_enum_values(enum_type: Type[Enum]) -> List:
    """
    Gets all the possible enumerations of an enum.
    """
    return [e.value for e in enum_type]


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def to_snake_case(string: str) -> str:
    """
    This func gets a string in any case and return it in snakecase.
    Args:
        string (): string to snakecase

    Returns:
        snakecase string
    """
    string = string.replace(" ", "_")
    string = string.replace("-", "_")
    string = string.replace(".", "_")
    snake_case_word = string[0]
    for char in string[1:]:
        if char.isupper() and snake_case_word[-1].islower():
            snake_case_word += f"_{char}"
        else:
            snake_case_word += char
    return snake_case_word.lower()


def to_title_case(string: str) -> str:
    """
    This func gets a string in any case and return it in titlecase.
    Args:
        string (): string to titlecae

    Returns:
        titlecase string
    """
    string = string.replace("_", " ")
    string = string.replace("-", " ")
    string = string.replace(".", " ")
    return_string = string[0].upper()
    for inx, char in enumerate(string[1:]):
        if char.isupper():
            if string[1:][inx - 1].islower():
                return_string += " "
        return_string += char
    return " ".join([word[0].upper() + word[1:] for word in return_string.lower().split(" ")])


def get_all_enum_fields_in_web_form(enum, custom: Dict = {}) -> List[str]:
    """
        This function made to serve the platform ui.

    Args:
        enum ():  deci enum class to rescue values from.
        custom (): dict: key - value of field of the enum, value- the value to set the key to. instead of camel case.

    Returns:
        all enum fields transformed to camelCase if not in custom. ex:  'object_detection' to 'objectDetection'
    """
    return get_all_list_fields_in_web_form(list_of_fields=get_enum_values(enum), custom=custom)


def get_all_list_fields_in_web_form(list_of_fields, custom: Dict = {}) -> List[str]:
    """
        This function made to serve the platform ui.

    Args:
        list_of_fields (): list of values to convert to web form.
        custom (): dict: key - one of the values of field of the list, value- the value to set the key to. instead of camel case.

    Returns:
        all list fields transformed to camel case if not in custom. ex:  'object_detection' to 'objectDetection'.
    """
    fields = []
    for field in list_of_fields:
        if field in custom.keys():
            field = custom[field]
        else:
            field = to_title_case(field)
        fields.append(field)
    return fields
