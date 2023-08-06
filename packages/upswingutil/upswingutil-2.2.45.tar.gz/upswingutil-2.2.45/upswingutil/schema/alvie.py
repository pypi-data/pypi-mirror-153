from typing import Optional
from pydantic import BaseModel


class AlvieRating(BaseModel):
    overall: Optional[int] = 0
    foodAndBev: Optional[int] = 0
    roomService: Optional[int] = 0
    roomQuality: Optional[int] = 0
    ambience: Optional[int] = 0


class Alvie(BaseModel):
    rating: Optional[AlvieRating] = AlvieRating()
    comments: Optional[list] = []