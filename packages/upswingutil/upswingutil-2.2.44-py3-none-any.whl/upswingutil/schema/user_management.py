from typing import List, Optional

from pydantic.main import BaseModel


class BookingsModel(BaseModel):
    hotelId: str
    reservationId: str
    roomId: str


class GuestUserProfileModel(BaseModel):
    # hotelId: str = "11282"
    profileSource: str = 'manual'
    firstName: str
    lastName: str
    email: str
    mobile: str
    bookings: Optional[List[BookingsModel]] = None
