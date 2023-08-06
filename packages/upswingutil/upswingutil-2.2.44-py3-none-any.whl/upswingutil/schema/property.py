from typing import Optional, List
from pydantic import BaseModel


class MultiText(BaseModel):
    defaultText: str = ''
    translatedTexts: Optional[list] = []


class PropertyPrimaryDetails(BaseModel):
    legalOwner: str


class PropertyGeneralInformation(BaseModel):
    roomCount: int
    floorCount: int = 0
    checkInTime: str = ''
    checkOutTime: str = ''
    hotelInfoWebsite: str
    longitude: float = None
    latitude: float = None
    baseLanguage: str = 'E'


class PropertyCurrencyFormatting(BaseModel):
    currencyCode: str = ''
    currencyFormat: str = ''
    decimalPositions: str = ''


class PropertyControls(BaseModel):
    class PropertySellControl(BaseModel):
        startDate: str = None

    class CurrencyFormatting(BaseModel):
        currencyCode: str = 'USD'
        currencyFormat: str = ''
        decimalPositions: int = 2

    class CateringCurrencyFormatting(BaseModel):
        currencyCode: str = 'USD'
        currencyFormat: str = ''

    class DateTimeFormatting(BaseModel):
        longDateFormat: str = ''
        shortDateFormat: str = ''
        timeFormat: str = ''
        timeZoneRegion: str = ''

    class ApplicationMode(BaseModel):
        mbsSupported: Optional[bool] = False

    sellControls: PropertySellControl = PropertySellControl()
    currencyFormatting: CurrencyFormatting = CurrencyFormatting()
    cateringCurrencyFormatting: CateringCurrencyFormatting = CateringCurrencyFormatting()
    dateTimeFormatting: DateTimeFormatting = DateTimeFormatting()
    applicationMode: ApplicationMode = ApplicationMode()


class PropertyCommunication(BaseModel):
    phoneNumber: str = ''
    email: str = None


class PropertyAddress(BaseModel):
    class CountryInfo(BaseModel):
        code: str = ''

    addressLine: list
    cityName: str = ''
    postalCode: str = ''
    state: str = ''
    country: CountryInfo
    regionCode = "NA"


class PropertyAttractions(BaseModel):
    name: str
    address: Optional[dict]
    operationHours: Optional[str]
    code: str


class PropertyBuilding(BaseModel):
    code: str
    description: str
    rooms: List[str]
    credits: Optional[int]


class PropertyRoom(BaseModel):
    class RoomType(BaseModel):
        pseudo: bool
        suite: bool
        roomClass: str
        houseKeeping: bool
        minimumOccupancy: Optional[int] = 0
        maximumOccupancy: Optional[int] = 0
        accessible: bool
        roomType: str
        meetingRoom: bool

    class RoomFeatures(BaseModel):
        code: str
        description: str
        orderSequence: int

    class ConnectingRoom(BaseModel):
        roomId: str

    roomType: Optional[RoomType]
    roomFeatures: List[RoomFeatures] = []
    roomDescription: str
    accessible: Optional[bool] = False
    roomId: str
    meetingRoom: Optional[bool] = False
    roomComponents: Optional[list] = []
    connectingRooms: Optional[List[ConnectingRoom]] = []
    rateAmount: Optional[dict] = {}
    maximumOccupancy: Optional[int] = 0
    sellSequence: Optional[int]
    keyOptions: Optional[list] = []
    turndownService: Optional[bool]
    roomSection: Optional[dict] = {}


class PropertyRoomClass(BaseModel):
    class RoomTypes(BaseModel):
        class RoomType(BaseModel):
            roomClass: str
            shortDescription: str
            pseudo: bool
            accessible: bool
            sendToInterface: bool
            sellSequence: int = 0
            suite: bool
            meetingRoom: bool
            roomType: str
            numberOfRooms: int
            inactive: bool

        roomTypeSummary: List[RoomType] = []

    description: MultiText = MultiText()
    sequence: int
    code: str
    inactive: bool
    roomTypes: RoomTypes


class PropertyAirport(BaseModel):
    description: str
    distance: str
    distanceType: str
    direction: str
    transportationOptions: Optional[list] = []
    code: str


class PropertyTransportation(BaseModel):
    transportationCode: str
    priceRange: str
    description: str
    relativePosition: Optional[dict] = {}
    phoneNumber: str


class PropertyCreditCardTypes(BaseModel):
    code: str
    description: MultiText = MultiText()


class PropertyHotelAmenities(BaseModel):
    description: str
    featureCode: str
    orderSequence: Optional[int] = -1
    amenityType: str
    beginDate: str


class PropertyAccountsReceivableDetails(BaseModel):
    accountName: str
    accountId: Optional[dict] = {}
    accountNo: str
    profileId: Optional[dict] = {}
    creditLimit: Optional[dict] = {}
    contactName: str
    monthEndCalcYN: bool
    address: Optional[dict] = {}
    email: Optional[dict] = {}
    status: Optional[dict]
    batchStatement: bool
    printFoliosWithStatement: bool
    emailStatementsReminders: bool
    primary: bool
    type: str
    accountTypeDescription: str
    permanent: bool


class PropertyFrontOfficeStats(BaseModel):
    code: str
    value: int


class Property(BaseModel):
    id: str
    name: str = ''
    hotelId: str = ''
    orgId: str = ''
    primaryDetails: PropertyPrimaryDetails
    generalInformation: PropertyGeneralInformation
    accommodationDetails: dict = {}
    propertyControls: PropertyControls = PropertyControls()
    communication: PropertyCommunication
    address: PropertyAddress
    hotelRateRanges: Optional[list]
    alternateHotels: Optional[list]
    hotelCorporateInformations: Optional[dict]
    # attractions: List[PropertyAttractions] = []
    buildings: Optional[List[PropertyBuilding]] = []
    rooms: List[PropertyRoom]
    roomHierarchies: Optional[list] = []
    roomClasses: Optional[List[PropertyRoomClass]] = []


if __name__ == '__main__':
    model = Property(
        id=1,
        name="happy",
        clientId='123',
        orgId='11249',
        primaryDetails={'legalOwner': 'Fam Living'},
        generalInformation={'roomCount': 10, 'hotelInfoWebsite': 'https://oracle.com'},
        communication={'phoneNumber': '1234', 'email': 'test@gmail.com'},
        address={'addressLine': [], 'cityName': 'Dubai', 'postalCode': '20232', 'state': 'Dubai',
                 'country': {'code': 'UAE'}, 'regionCode': 'AS'},
        rooms=[
            {
                'roomId': 1,
                'roomDescription': 'abcd',
                'maximumOccupancy': 2
            }
        ]
    )

    print(model.dict())
