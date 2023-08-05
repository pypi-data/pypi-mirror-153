from datetime import datetime

from pydantic import BaseModel
from stringcase import camelcase


def to_camel(string):
    return camelcase(string)


class Schema(BaseModel):
    """
    A base class for all of Deci's model classes.
    A model stores data in constant fields, and let us manipulate the data in a more readable way.
    """

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        validate_assignment = True

    pass


class DBSchema(Schema):
    update_time: datetime = None
    creation_time: datetime = None
