from typing import Union
from pydantic import BaseModel


class DataStructure(BaseModel):
    status: int = 200
    code: str = '000000'
    success: bool = False
    message: str = ''
    data: Union[dict, list] = None

    def as_dict(self) -> dict:
        return self.__dict__
