from typing import Optional
from pydantic import BaseModel


class Country(BaseModel):
    orgId: str
    clientId: Optional[list] = []
    name: str
    statisticCode: str
    guestAddressFormat: str
    regionCode: str
    region: str
    isoCode: str
    displayFlag: bool
    countryCode: str
