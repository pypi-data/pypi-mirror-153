from typing import Optional
from pydantic import BaseModel

class MultiText(BaseModel):
    defaultText: str = ''
    translatedTexts: Optional[list] = []

# class Languages(BaseModel):
#     description: MultiText = MultiText()
#     translationLanguageCode: str
#     reportDateLanguage: str = ''
#     languageCode = str

class CommunicationMethodsEntDetails(BaseModel):
    code: str
    description: MultiText = MultiText()
    displayOrder: int

class HotelTaxType(BaseModel):
    code: str
    description: str
    collectingAgentTax: Optional[bool]
    printAutoAdjust: Optional[bool]
    reportExemptDays: int
    reportTaxPercentage: int


class LeisureActivityTypes(BaseModel):
    typeCode: str
    description: str

class BlockReservationMethodCodes(BaseModel):
    code: str
    description: MultiText = MultiText()
    displayOrder: int


