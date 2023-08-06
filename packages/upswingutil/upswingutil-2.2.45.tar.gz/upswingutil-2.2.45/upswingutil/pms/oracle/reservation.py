import json

from upswingutil.pms.oracle import NAME, get_key, validate_key
from upswingutil.db import Mongodb, Firestore, MongodbV2
from upswingutil.schema import Token
from datetime import datetime, timedelta
import requests
import logging
from upswingutil.db.model import ReservationModel, Status, ReservationGuestInfo, ReservationGuestShort, GuestsModel


def _get_status(status):
    if status == 'NoShow':
        return Status.NO_SHOW
    elif status == 'CheckedOut':
        return Status.DEPARTED
    elif status == 'Reserved':
        return Status.RESERVED
    elif status == 'Cancelled':
        return Status.CANCELLED
    elif status == 'InHouse':
        return Status.IN_HOUSE
    else:
        print(status)
        return Status.UNCONFIRMED


def _get_id(record):
    _id = next((x['id'] for x in record.get('reservationIdList') if x['type'] == 'Reservation'), None)
    return _id


def _get_transaction_info(transactions):
    return transactions


def _get_package_info(package):
    del package['transactionDate']
    return package


def _generate_day_to_day_entry(record):
    entry_list = list()
    room_rates = record.get('roomStay').get('roomRates')
    start_date = datetime.fromisoformat(record.get('roomStay').get('arrivalDate'))
    end_date = datetime.fromisoformat(record.get('roomStay').get('departureDate'))
    day_delta = timedelta(days=1)
    for i in range((end_date - start_date).days):
        _rates = next((x for x in room_rates if x['start'] == str((start_date + i * day_delta).date())), None)
        _activity = {
            'date': str((start_date + i * day_delta).date()),
            'day_of_stay': i + 1
        }
        if _rates:
            _activity.update(_rates)
        else:
            print('No entry on given date', ((start_date + i * day_delta).date()))
        entry_list.append(_activity)
    return entry_list


def _get_folio_information(record):
    data = {
        'folioWindows': record.get('folioWindows'),
        'folioHistory': record.get('folioHistory')
    }
    return data


def _get_geo_region(nationalID: int):
    result = 'unknown'
    try:
        mongo = Mongodb('upswing')
        region = mongo.get_collection('countries').find_one({"_id": nationalID}, {"region": 1})
        mongo.close_connection()
        result = region if region else 'unknown'
    except Exception as e:
        logging.error(f'Error getting geo region of nation {nationalID}')
        logging.error(e)
    finally:
        return result


@DeprecationWarning
class ReservationSync:

    def __init__(self, orgId: str, g_cloud_token=None):
        self.orgId = orgId
        self.mongo = Mongodb(orgId)
        self.mongoV2 = MongodbV2(orgId)
        self.token: Token = get_key(self.orgId)
        self.g_cloud_token = g_cloud_token
        self._api_call_counter = 0

    def _extract_guest_profile(self, hotelId, guest):
        try:
            guestId = 0
            for item in guest.get('profileInfo').get('profileIdList'):
                if item.get('type') == 'Profile':
                    guestId = item.get('id')

            if not validate_key(self.token.validity):
                logging.info(f'Refreshing {NAME} token as it is about to expire')
                self.token = get_key(self.orgId, self.token.refreshKey)

            _url = f'{self.token.hostName}/crm/v1/profiles/{guestId}?fetchInstructions=Address' \
                   f'&fetchInstructions=Comment&fetchInstructions=Communication&fetchInstructions=Correspondence' \
                   f'&fetchInstructions=DeliveryMethods&fetchInstructions=FutureReservation' \
                   f'&fetchInstructions=GdsNegotiatedRate&fetchInstructions=HistoryReservation' \
                   f'&fetchInstructions=Indicators&fetchInstructions=Keyword&fetchInstructions=Membership' \
                   f'&fetchInstructions=NegotiatedRate&fetchInstructions=Preference&fetchInstructions=Profile' \
                   f'&fetchInstructions=Relationship&fetchInstructions=SalesInfo&fetchInstructions=Subscriptions' \
                   f'&fetchInstructions=WebUserAccount'
            _profile_data = self.retrieve_data(hotelId, _url)
            if _profile_data:
                idObj = dict()
                for item in _profile_data['profileIdList']:
                    idObj[item.get('type').lower()] = item['id']
                _profile_data['idObj'] = idObj
                _profile_data['birthDate'] = guest.get('birthDate')
                return _profile_data
            else:
                logging.error(f'Guest profile not found : {guestId}')

        except Exception as e:
            logging.error(f'Error while transforming guest {guest}')
            logging.error(e)

    def _get_guest_list(self, hotelId, record):
        logging.info(f'Processing guest list of size: {len(record.get("reservationGuests"))}')
        _guest_list = list()
        for item in record.get('reservationGuests'):
            _guest_profile = self._transform_guest_profile(self._extract_guest_profile(hotelId, item))
            self.mongoV2.save(_guest_profile)
            _guest = ReservationGuestShort(
                guest=_guest_profile,
                primary=item.get('primary'),
                birthDate=item.get('birthDate'),
                arrivalTransport=item.get('arrivalTransport'),
                departureTransport=item.get('departureTransport')
            )
            _guest_list.append(_guest)
        return _guest_list

    def _get_guest_info(self, record):
        guest_info = ReservationGuestInfo(
            adults=record.get('roomStay').get('guestCounts').get('adults'),
            children=record.get('roomStay').get('guestCounts').get('children'),
            infants=0,
            childBuckets=record.get('roomStay').get('guestCounts').get('childBuckets'),
            preRegistered=record.get('preRegistered'),
            guest_list=self._get_guest_list(record.get('hotelId'), record)
        )
        return guest_info

    def _transform_guest_profile(self, record):
        details = record.get('profileDetails')
        guest = GuestsModel(
            _id=record.get('idObj').get('profile'),
            idObj=record.get('idObj'),
            birthDate=record.get('birthDate'),
            profileType=details.get('profileType'),
            statusCode=details.get('statusCode'),
            registeredProperty=details.get('registeredProperty'),
            createDateTime=details.get('createDateTime'),
            creatorId=details.get('creatorId'),
            lastModifyDateTime=details.get('lastModifyDateTime'),
            lastModifierId=details.get('lastModifierId'),
            markForHistory=details.get('markForHistory'),
            keywords=details.get('keywords').get('keyword'),
            emails=details.get('emails'),
            telephones=details.get('telephones'),
            addresses=details.get('addresses'),
            profileMemberships=details.get('profileMemberships'),
            relationships=details.get('relationships'),
            stayReservationInfoList=details.get('stayReservationInfoList'),
            lastStayInfo=details.get('lastStayInfo'),
            profileAccessType=details.get('profileAccessType'),
            profileRestrictions=details.get('profileRestrictions'),
            privacyInfo=details.get('privacyInfo'),
            taxInfo=details.get('taxInfo'),
            salesInfo=details.get('salesInfo'),
            subscriptions=details.get('subscriptions'),
            mailingActions=details.get('mailingActions'),
            relationshipsSummary=details.get('relationshipsSummary'),
            preferenceCollection=details.get('preferenceCollection'),
            comments=details.get('comments'),
            profileDeliveryMethods=details.get('profileDeliveryMethods'),
            profileIndicators=details.get('profileIndicators'),
            customer=details.get('customer'),
            company=details.get('company'),
        )

        if details.get('profileType') == 'Guest':
            guest.firstName = details.get('customer').get('personName')[0].get('givenName')
            guest.middleName = details.get('customer').get('personName')[0].get('nameSuffix')
            guest.lastName = details.get('customer').get('personName')[0].get('surname')
        elif details.get('profileType') == 'Group':
            guest.firstName = details.get('company').get('companyName')
        else:
            logging.error(
                f'Unhandled profile type : {details.get("profileType")} for guest {record.get("idObj").get("profile")}')
        return guest

    def _get_reservation_id(self, idList, agent, hotelId, resv):
        resv_dict = dict()
        resv_dict['globalId'] = f'{agent}-{self.orgId}-{hotelId}-{resv}'
        for item in idList:
            value = item['id']
            _type = item['type']
            resv_dict[_type.lower()] = value
        return resv_dict

    def retrieve_data(self, clientId, url, payload="") -> dict:
        headers = {
            'Content-Type': 'application/json',
            'x-hotelid': clientId,
            'x-app-key': self.token.appKey,
            'Authorization': f'Bearer {self.token.key}'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self._api_call_counter += 1
        if response.status_code == 200:
            return dict(response.json())
        else:
            logging.error(f'Failed to retrieve data, status: {response.status_code}')
            logging.error(response.reason)
            return None

    def _extract_reservation_details(self, record):
        resv_id = record.get('id')
        try:
            hotel_id = record.get('hotelId')
            record['idObj'] = self._get_reservation_id(record.get('reservationIdList'), record.get('agent'), record.get('hotelId'), record.get('id'))
            logging.info(f"Extracting reservation {resv_id} additional details.")
            if self.token is None:
                self.token: Token = record.get('token')

            if not validate_key(self.token.validity):
                logging.info(f'Refreshing {NAME} token as it is about to expire')
                self.token = get_key(self.orgId, self.token.refreshKey)

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/cancellationHistory'
            data = self.retrieve_data(record.get('hotelId'), _url)
            record['cancellation'] = data.get('cxlActivityLog') if data else None

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/linkedSummary'
            data = self.retrieve_data(record.get('hotelId'), _url)
            record['linkedReservation'] = data.get('linkedReservationList') if data else None

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/calls'
            data = self.retrieve_data(record.get('hotelId'), _url)
            record['callHistory'] = data.get('callHistory') if data else None

            _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/inventoryItems'
            data = self.retrieve_data(record.get('hotelId'), _url)
            record['inventoryItems'] = data.get('inventoryItems') if data else None

            _url = f'{self.token.hostName}/csh/v0/hotels/{hotel_id}/reservations/{resv_id}/folios?includeFolioHistory=true&fetchInstructions=Account&fetchInstructions=Payee&fetchInstructions=Totalbalance&fetchInstructions=Windowbalances&fetchInstructions=Payment&fetchInstructions=Postings&fetchInstructions=Transactioncodes&fetchInstructions=Reservation'
            data = self.retrieve_data(record.get('hotelId'), _url)
            record['folioInformation'] = data.get('reservationFolioInformation') if data else None

            _url = f'{self.token.hostName}/csh/v0/hotels/{hotel_id}/transactions?reservationList={resv_id}&idContext=OPERA&type=Reservation&includeGenerates=true&includeTransactionsWithFolioNo=true&includeTransactionsWithManualPostingOnly=true'
            data = self.retrieve_data(record.get('hotelId'), _url)
            if data:
                del data['links']
            record['transactions'] = data

            return record
        except Exception as e:
            logging.error(f'Error retrieving addition reservation details for {resv_id}')
            logging.error(e)

    def _extract_reservation(self, record):
        try:
            reservationId = record.get("reservation")["reservation"]
            hotelId = record.get('reservation')['hotelId']
            logging.info(f'Extracting reservation: {reservationId}')

            header = {
                'Content-Type': 'application/json',
                'x-hotelid': hotelId,
                'x-app-key': self.token.appKey,
                'Authorization': f'Bearer {self.token.key}'
            }

            url = f"{self.token.hostName}/rsv/v1/hotels/{hotelId}/reservations/{reservationId}?fetchInstructions" \
                  f"=Comments&fetchInstructions=GuestMemberships&fetchInstructions=GuestLastStay&fetchInstructions" \
                  f"=ProfileAwards&fetchInstructions=ScheduledActivities&fetchInstructions=ServiceRequests" \
                  f"&fetchInstructions=ReservationAwards&fetchInstructions=RevenuesAndBalances&fetchInstructions" \
                  f"=Tickets&fetchInstructions=GuestComments&fetchInstructions=Packages&fetchInstructions" \
                  f"=InventoryItems&fetchInstructions=ReservationPaymentMethods&fetchInstructions=RoutingInstructions" \
                  f"&fetchInstructions=Preferences&fetchInstructions=Memberships&fetchInstructions=Alerts" \
                  f"&fetchInstructions=Traces&fetchInstructions=ConfirmationLetters&fetchInstructions=CallHistory" \
                  f"&fetchInstructions=FixedCharges&fetchInstructions=GuestMessages&fetchInstructions" \
                  f"=ReservationPolicies&fetchInstructions=Indicators&fetchInstructions=LinkedReservations" \
                  f"&fetchInstructions=ECoupons&fetchInstructions=TrackItItems&fetchInstructions=WebRegistrationCards" \
                  f"&fetchInstructions=ServiceRequests&fetchInstructions=ReservationActivities&fetchInstructions" \
                  f"=PrepaidCards&fetchInstructions=Shares&fetchInstructions=Attachments&fetchInstructions=Locators" \
                  f"&fetchInstructions=TransactionDiversions&fetchInstructions=ECertificates&fetchInstructions" \
                  f"=UpsellInfo&fetchInstructions=RoomAssignedByAI&fetchInstructions=Reservation"
            response = requests.request("GET", url, headers=header)
            self._api_call_counter += 1
            if response.status_code == 200:
                response_json = dict(response.json()).get('reservations').get('reservation')
                if len(response_json) > 0:
                    result = response_json[0]
                    result['id'] = reservationId
                    result['token'] = self.token
                    result['orgId'] = record.get('orgId')
                    result['agent'] = record.get('agent')
                    return result
                else:
                    logging.error(f"{NAME} returned reservation {reservationId} of length zero")
            else:
                logging.error(f"{NAME} returned status code {response.status_code} for reservation {reservationId} ")
        except Exception as err:
            logging.error(f'{record} load failed due to {err}')
        return None

    def _transform_reservation(self, record):
        reservationV2 = ReservationModel(
            _id=record.get('id'),
            hotelId=record.get('hotelId'),
            orgId=self.orgId,
            idObj=record.get('idObj'),
            agent=record.get('agent'),
            hotelName=record.get('folioInformation').get('reservationInfo').get('hotelName'),
            arrivalDate=record.get('roomStay').get('arrivalDate'),
            departureDate=record.get('roomStay').get('departureDate'),
            expectedTimes={
                'arrival': record.get('roomStay').get('expectedTimes').get('reservationExpectedArrivalTime'),
                'departure': record.get('roomStay').get('expectedTimes').get('reservationExpectedDepartureTime')
            },
            originalTimeSpan=record.get('roomStay').get('originalTimeSpan'),
            status=_get_status(record.get('reservationStatus')),
            alerts=record.get('alerts'),
            metaInfo={
                'allowAutoCheckin': record.get('allowAutoCheckin'),
                'allowMobileCheckout': record.get('allowMobileCheckout'),
                'allowMobileViewFolio': record.get('allowMobileViewFolio'),
                'allowPreRegistration': record.get('allowPreRegistration'),
                'allowedActions': record.get('allowedActions'),
                'computedReservationStatus': record.get('computedReservationStatus'),
                'creatorId': record.get('creatorId'),
                'postStayChargeAllowed': record.get('folioInformation').get('postStayChargeAllowed'),
                'preStayChargeAllowed': record.get('folioInformation').get('preStayChargeAllowed'),
                'autoCheckInAllowed': record.get('folioInformation').get('autoCheckInAllowed'),
                'postToNoShowCancelAllowed': record.get('folioInformation').get('postToNoShowCancelAllowed'),
                'stampDutyExists': record.get('folioInformation').get('stampDutyExists'),
                'roomAndTaxPosted': record.get('folioInformation').get('roomAndTaxPosted'),
                'hasOpenFolio': record.get('hasOpenFolio'),
                'lastModifierId': record.get('lastModifierId'),
                'optedForCommunication': record.get('optedForCommunication'),
                'walkIn': record.get('walkIn'),
                'printRate': record.get('printRate'),
                'remoteCheckInAllowed': record.get('roomStay').get('remoteCheckInAllowed'),
                'roomNumberLocked': record.get('roomStay').get('roomNumberLocked'),
                'roomStayReservation': record.get('roomStayReservation'),
                'reservationIndicators': record.get('reservationIndicators'),
                'routingInstructions': record.get('routingInstructions')
            },
            createBusinessDate=record.get('createBusinessDate'),
            createDateTime=record.get('createDateTime'),
            guestLocators=record.get('guestLocators'),
            lastModifyDateTime=record.get('lastModifyDateTime'),
            bookingInfo={
                'upgradeEligible': record.get('upgradeEligible'),
                'bookingMedium': record.get('roomStay').get('bookingMedium'),
                'bookingMediumDescription': record.get('roomStay').get('bookingMediumDescription'),
                'guarantee': record.get('roomStay').get('guarantee'),
                'sourceOfSaleType': record.get('sourceOfSale').get('sourceType'),
                'sourceOfSaleCode': record.get('sourceOfSale').get('sourceCode'),
            },
            financeInfo={
                'totalPoints': record.get('roomStay').get('totalPoints'),
                'totalSpending': record.get('roomStay').get('total'),
                'paymentMethod': record.get('reservationPaymentMethods'),
                'revenueBucketsInfo': record.get('revenueBucketsInfo'),
                'transactions': _get_transaction_info(record.get('transactions')),
                'revenue': record.get('cashiering')
            },
            daily_activity=_generate_day_to_day_entry(record),
            linkedReservation=record.get('linkedReservation'),
            guestInfo=self._get_guest_info(record),
            eCertificates=record.get('eCertificates'),
            historyEvents=record.get('callHistory'),
            cancellation=record.get('cancellation'),
            comments=record.get('comments'),
            policies=record.get('reservationPolicies'),
            inventoryItems=record.get('inventoryItems'),
            preferences=record.get('preferenceCollection'),
            memberships=record.get('reservationMemberships'),
            packages=record.get('reservationPackages'),
            auraRecordUpdatedOn=str(datetime.now())
        )

        if record.get('folioInformation'):
            _f_info = record.get('folioInformation')
            reservationV2.folioInformation = _get_folio_information(_f_info)
            reservationV2.roomStay = _f_info.get('reservationInfo').get('roomStay')
            reservationV2.financeInfo['taxType'] = _f_info.get('reservationInfo').get('taxType')
            reservationV2.financeInfo['commissionPayoutTo'] = _f_info.get('reservationInfo').get('commissionPayoutTo'),
            del _f_info

        return reservationV2

    def _load_to_mongodb(self, record):

        try:
            logging.info(f'Adding reservation {record.id} to db {record.orgId}')
            self.mongo.get_collection(self.mongo.RESERVATION_COLLECTION).update_one({'_id': record.id},
                                                                          {'$set': record.dict(exclude={'token', 'id'})}, upsert=True)
        except Exception as e:
            logging.error(f'Error storing to respective {record.id} to db {record.orgId}')
            logging.error(e)

    def _load_to_alvie(self, record: ReservationModel):
        firestore_db = Firestore(app='alvie')
        guest_list = [item["idObj"] for item in record.guestInfo.get('guest_list')]
        user_email_list = []
        resv_info = {
            "_id": record.id,
            "agent": record.agent,
            "orgId": record.orgId,
            "areaId": record.roomStay,
            "arrivalDate": record.arrivalDate,
            "departureDate": record.departureDate,
            "propertyId": record.hotelId,
            "propertyName": record.hotelName,
            "status": record.status,
            "travelAgentId": record.bookingInfo.get('sourceOfSaleCode'),
            "travelAgentName": record.bookingInfo.get('sourceOfSaleType')
        }
        logging.debug(f"Final reservation id : {record.id}")
        for email in user_email_list:
            docs = firestore_db.get_collection('users').where("email", "==", email).stream()
            for doc in docs:
                logging.info("loading reservation to alvie")
                firestore_db.get_collection(f'users/{doc.id}/reservations') \
                    .document(str(record.id)) \
                    .set(resv_info, merge=True)
                logging.debug(f"added to {doc.id}")

    def process(self, reservationId, hotelId):
        record = {
            'orgId': self.orgId,
            'agent': NAME,
            'reservation': {
                'reservation': reservationId,
                'hotelId': hotelId
            }
        }

        if not validate_key(self.token.validity):
            logging.info(f'Refreshing {NAME} token as it is about to expire')
            self.token = get_key(self.orgId, self.token.refreshKey)

        record = self._extract_reservation(record)
        if record:
            record = self._extract_reservation_details(record)
            record = self._transform_reservation(record)
            self.mongoV2.save(record)
            # self._load_to_alvie(record)

    def __del__(self):
        logging.info(f'API calls made: {self._api_call_counter}')
        if self.mongo:
            self.mongo.close_connection()
        if self.mongoV2:
            self.mongoV2.close_connection()
