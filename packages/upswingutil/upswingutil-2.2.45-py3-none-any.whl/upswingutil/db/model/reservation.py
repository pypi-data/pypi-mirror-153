from enum import Enum

from mongoengine import *
from upswingutil.db.model import ProfileIDObject, GuestsModel


class Status(Enum):
    NO_SHOW = 'NoShow'
    DEPARTED = 'Departed'
    RESERVED = 'Reserved'
    CANCELLED = 'Cancelled'
    ARRIVED = 'Arrived'
    CONFIRMED = 'Confirmed'
    CREATED = 'Created'
    UNCONFIRMED = 'Unconfirmed'
    MAINTENANCE = 'Maintenance'
    IN_HOUSE = 'InHouse'
    PENCIL = 'Pencil'


class ReservationIDObj(DynamicEmbeddedDocument):
    reservation = StringField()
    confirmation = StringField()
    globalId = StringField()


class AlvieReservationModel(DynamicEmbeddedDocument):
    comments = ListField(StringField())
    rating = DictField()


class ReservationGuestShort(DynamicEmbeddedDocument):
    idObj = EmbeddedDocumentField(ProfileIDObject)
    primary = BooleanField()
    arrivalTransport = DictField()
    departureTransport = DictField()
    # birthDate = StringField()
    guest = ReferenceField(GuestsModel)


class ReservationGuestInfo(DynamicEmbeddedDocument):
    adults = IntField()
    children = IntField()
    infants = IntField()
    childBuckets = DictField()
    preRegistered = BooleanField()
    guest_list = EmbeddedDocumentListField(ReservationGuestShort)


class ReservationModel(DynamicDocument):
    meta = {'collection': 'reservations'}

    _id = StringField(required=True, primary_key=True)
    agent = StringField(required=True)
    alvie = EmbeddedDocumentField(AlvieReservationModel)
    arrivalDate = StringField(required=True)
    bookingInfo = DictField()
    historyEvents = ListField(DictField())
    cancellation = ListField(DictField())
    comments = ListField(DictField())
    createBusinessDate = StringField()
    createDateTime = StringField()
    daily_activity = ListField(DictField())
    departureDate = StringField()
    eCertificates = ListField(DictField())
    expectedTimes = DictField()
    financeInfo = DictField()
    folioInformation = DictField()
    guestInfo = EmbeddedDocumentField(ReservationGuestInfo)
    guestLocators = DictField()
    hotelId = StringField(required=True)
    hotelName = StringField(required=True)
    idObj = EmbeddedDocumentField(ReservationIDObj)
    inventoryItems = DictField()
    linkedReservation = DictField()
    memberships = ListField(DictField())
    metaInfo = DictField()
    orgId = StringField()
    originalTimeSpan = DictField()
    packages = ListField(DictField())
    policies = DictField()
    preferences = ListField(DictField())
    housekeeping = ListField(DictField())
    roomStay = DictField()
    status = EnumField(Status, default=Status.CREATED, required=True)
    auraRecordUpdatedOn = StringField()


class ReservationModelV2(DynamicDocument):
    meta = {'collection': 'reservations'}

    _id = StringField(required=True, primary_key=True)
    orgId = StringField()
    idObj = EmbeddedDocumentField(ReservationIDObj)
    agent = StringField(required=True)
    datesAndDuration = DictField()
    status = EnumField(Status, default=Status.CREATED, required=True)
    correspondence = ListField(DictField())
    metaInfo = DictField()
    property = DictField(required=True)
    stayInfo = DictField(required=True)
    reservationTypes = DictField(required=True)
    bookingInfo = DictField(required=True)
    financeInfo = DictField(required=True)
    daily_activity = ListField(DictField())
    linkedReservation = ListField(DictField())
    guestInfo = EmbeddedDocumentField(ReservationGuestInfo)
    eCertificates = ListField(DictField())
    historyEvents = ListField(DictField())
    cancellation = ListField(DictField())
    housekeeping = ListField(DictField())
    comments = ListField(DictField())
    policies = DictField()
    inventoryItems = DictField()
    preferences = ListField(DictField())
    requirement = ListField(DictField())
    rego_access = ListField(DictField())
    memberships = ListField(DictField())
    packages = ListField(DictField())
    transfers = ListField(DictField())
    event = DictField()
    alvie = EmbeddedDocumentField(AlvieReservationModel)
    auraRecordUpdatedOn = DateTimeField()
