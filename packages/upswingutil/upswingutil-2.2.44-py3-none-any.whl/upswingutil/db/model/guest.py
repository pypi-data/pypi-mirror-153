from mongoengine import *


class ProfileIDObject(DynamicEmbeddedDocument):
    profile = StringField()
    corporateId = StringField()


class GuestsModel(DynamicDocument):
    meta = {'collection': 'guests'}

    _id = StringField(primary_key=True)
    birthDate = StringField()
    addresses = DictField()
    comments = DictField()
    createDateTime = StringField()
    creatorId = StringField()
    businessSegments = StringField()
    customer = DictField()
    company = DictField()
    emails = DictField()
    firstName = StringField()
    idObj = EmbeddedDocumentField(ProfileIDObject)
    keywords = ListField()
    lastModifierId = StringField()
    lastModifyDateTime = StringField()
    lastName = StringField()
    lastStayInfo = DictField()
    mailingActions = DictField()
    markForHistory = BooleanField()
    middleName = StringField()
    preferenceCollection = DictField()
    privacyInfo = DictField()
    profileAccessType = DictField()
    profileDeliveryMethods = DictField()
    profileIndicators = ListField(DictField())
    profileMemberships = DictField()
    profileRestrictions = DictField()
    profileType = StringField()
    registeredProperty = StringField()
    relationships = DictField()
    relationshipsSummary = DictField()
    salesInfo = DictField()
    statusCode = StringField()
    stayReservationInfoList = DictField()
    subscriptions = ListField(DictField())
    taxInfo = DictField()
    telephones = DictField()


class GuestsModelV2(DynamicDocument):
    meta = {'collection': 'guests'}

    _id = StringField(primary_key=True)
    idObj = EmbeddedDocumentField(ProfileIDObject)
    profileType = StringField()
    title = StringField()
    firstName = StringField()
    lastName = StringField()
    datesAndDurations = DictField()
    address = DictField()
    contactInfo = DictField()
    privacyInfo = DictField()
    documents = DictField()
    metaInfo = DictField()
    company = DictField()
    registeredProperty = StringField()
    auraRecordUpdatedOn = DateTimeField()
