from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    key: str
    refreshKey: Optional[str] = ''
    validity: str
    hostName: str
    appKey: Optional[str] = ''
