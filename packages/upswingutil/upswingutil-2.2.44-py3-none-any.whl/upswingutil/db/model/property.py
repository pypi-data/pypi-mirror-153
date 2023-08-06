from mongoengine import *


class PropertyAddressModel(DynamicEmbeddedDocument):
    state = StringField()
    postalCode = StringField()
    cityName = StringField()
    regionCode = StringField()
    countryCode = StringField()
    addressLine = ListField(StringField())


class PropertyModel(DynamicDocument):
    meta = {'collection': 'properties'}

    _id = StringField(primary_key=True)
    name = StringField()
    orgId = StringField()
    clientId = StringField()
    hotelId = StringField()
    accommodationDetails = DictField()
    address = EmbeddedDocumentField(PropertyAddressModel)
    alternateHotels = ListField(DictField())
    buildings = ListField(DictField())
    communication = DictField()
    generalInformation = DictField()
    hotelCorporateInformations = DictField()
    hotelRateRanges = ListField(DictField())
    primaryDetails = DictField()
    propertyControls = DictField()
    roomClasses = ListField(DictField())
    roomHierarchies = ListField(DictField())
    rooms = ListField(DictField())
    airports = ListField(DictField())
    transportations = ListField(DictField())
    creditCardTypes = ListField(DictField())
    hotelAmenities = ListField(DictField())
    attractions = ListField(DictField())
    accountsReceivableDetails = ListField(DictField())
    taxType = ListField(DictField())
    leisureManagement = DictField()
    transactionCodes = ListField(DictField())
    cateringMenu = DictField()
    eventFunctionSpaces = ListField(DictField())
    eventForecasts = ListField(DictField())
    eventInventoryItems = ListField(DictField())
    eventCodes = ListField(DictField())
    activityConfigDetails = DictField()
    eventRevenueTypes = DictField()
    ratePlan = DictField()
    

if __name__ == '__main__':
    import upswingutil as ul
    ul.MONGO_URI = 'mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSource=admin&readPreference=primary&appname=Agent%20Oracle%20Dev&ssl=false'
    from upswingutil.db import MongodbV2
    mongo = MongodbV2('OHIPSB2')
    prop = PropertyModel(_id='SAND02')
    prop.orgId = 'OHIPSB2'
    prop.clientId = 'SAND020'
    prop.name = "SAmple"
    address = PropertyAddressModel()
    address.state = 'test'
    address.addressLine = ['sa', 'sdfs', 'test']
    address.cityName = 'temt2'
    prop.address = address
    prop.primaryDetails = {
        'legal': 'smwekmw'
    }
    mongo.save(prop)
    mongo.close_connection()
