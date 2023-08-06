from typing import List

from pydantic import BaseModel
from .auth import Token


class ReservationMsg(BaseModel):
    orgId: str
    agent: str
    token: Token
    reservations: List[dict]
