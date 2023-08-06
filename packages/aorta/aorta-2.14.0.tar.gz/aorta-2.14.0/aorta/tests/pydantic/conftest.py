# pylint: skip-file
import pydantic

import aorta


class PydanticCommand(aorta.Command):
    foo: int


class Model(pydantic.BaseModel):
    command: PydanticCommand
