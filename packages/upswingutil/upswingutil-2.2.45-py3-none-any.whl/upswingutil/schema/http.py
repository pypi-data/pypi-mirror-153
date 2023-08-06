from typing import List

from pydantic import BaseModel


class ResponseList(BaseModel):
    status: bool = False
    message: str = 'default error msg'
    data: List = []


class ResponseDict(BaseModel):
    status: bool = False
    message: str = 'default error msg'
    data: dict
