from upswingutil.pms import store_reservation_to_alvie
from upswingutil.pms.oracle import NAME, get_key, validate_key
from upswingutil.db import Mongodb, MongodbV2
from upswingutil.schema import Token
from datetime import datetime, timedelta
import requests
import logging
from upswingutil.db.model import ReservationModelV2, Status, ReservationGuestInfo, ReservationGuestShort, \
    GuestsModelV2


def _get_status(status):
    if status == 'NoShow':
        return Status.NO_SHOW
    elif status == 'CheckedOut' or status == 'Departed':
        return Status.DEPARTED
    elif status == 'Reserved':
        return Status.RESERVED
    elif status == 'Cancelled':
        return Status.CANCELLED
    elif status == 'InHouse':
        return Status.IN_HOUSE
    else:
        logging.error(f'Missing Status : {status}')
        return Status.UNCONFIRMED


def _get_id(record):
    _id = next((x['id'] for x in record.get('reservationIdList') if x['type'] == 'Reservation'), None)
    return _id


def _get_transaction_info(transactions):
    return transactions


def _get_package_info(package):
    return [{
        'packageCode': item.get('packageCode'),
        'ratePlanCode': item.get('ratePlanCode'),
        'source': item.get('source'),
        'description': item.get('packageHeaderType').get('primaryDetails').get('description'),
        'shortDescription': item.get('packageHeaderType').get('primaryDetails').get('shortDescription'),
        'amount': sum([x['unitPrice'] for x in item.get('scheduleList')]) * item.get('consumptionDetails').get(
            'totalQuantity')
    } for item in package] if package else []


def _generate_day_to_day_entry(record):
    _daily_activity = list()
    start_date = datetime.fromisoformat(record.get('roomStay').get('arrivalDate'))
    end_date = datetime.fromisoformat(record.get('roomStay').get('departureDate'))
    day_delta = timedelta(days=1)
    for i in range((end_date - start_date).days):
        _rates = next((x for x in record.get('roomStay').get('roomRates') if
                       x['start'] == str((start_date + i * day_delta).date())), None)
        _daily_activity.append({
            'date': str((start_date + i * day_delta).date()),
            'day_of_stay': i + 1,
            'roomType': _rates.get('roomType'),
            'ratePlanCode': _rates.get('ratePlanCode'),
            'rateTypeId': _rates.get('ratePlanCode'),
            'roomId': _rates.get('roomId'),
            'roomName': _rates.get('roomId'),
            'rates': {
                'currency': _rates.get('rates').get('rate')[0].get('base').get('currencyCode'),
                'amountBeforeTax': _rates.get('rates').get('rate')[0].get('base').get('amountBeforeTax'),
                'discountAmount': None,
                'packageAmount': None,
                'totalRateAmount': _rates.get('total').get('amountBeforeTax')
            },
            'revenue': {
                'accommodation': (
                            record.get('cashiering').get('revenuesAndBalances').get('roomRevenue').get('amount') / (
                                end_date - start_date).days),
                'accommodationTax': 0,
                'accommodationGST': 0,
                'foodAndBeverage': (record.get('cashiering').get('revenuesAndBalances').get('foodAndBevRevenue').get(
                    'amount') / (end_date - start_date).days),
                'foodAndBeverageTax': 0,
                'foodAndBeverageGST': 0,
                'other': 0,
                'otherTax': 0,
                'otherGST': 0
            },
            'guestCounts': {
                'adults': _rates.get('guestCounts').get('adults'),
                'children': _rates.get('guestCounts').get('children'),
                'infants': 0
            }
        })
    return _daily_activity


def _create_reservation_id_obj(record) -> dict:
    return {
        'reservation': str(record.get('id')),
        'globalId': f"{record.get('agent')}-{record.get('orgId')}-{record.get('clientId')}-{record.get('id')}",
        'onlineConfirmationId': str(record.get('idObj').get('confirmation')),
        'hotelId': str(record.get('hotelId')),
        'createdById': str(record.get('creatorId')),
        'modifiedById': str(record.get('lastModifierId')),
        'roomId': str(record.get('roomStay').get('roomRates')[0].get('roomId'))
    }


def _transform_cancellation_record(record, policy) -> list:
    _cancellation_list = list()
    for item in record:
        _cancellation_list.append({
            'reason': item.get('reason'),
            'cxlDate': item.get('cxlDate'),
            'userId': item.get('userId'),
            'policy': policy,
            'externalCancelId': None,
            'businessLostId': None
        })
    return _cancellation_list


def _create_guest_id_obj(record):
    return {
        'profile': str((next(x for x in record.get('profileIdList') if x['type'] == 'Profile')).get('id')),
        'corporateId': str((next(x for x in record.get('profileIdList') if x['type'] == 'CorporateId')).get('id'))
    }


def _get_contact_details(record):
    _data = dict()

    if record.get('emails'):
        _data['email'] = next((x['email']['emailAddress'] for x in record.get('emails').get('emailInfo') if
                               x['email']['primaryInd'] is True), '')
        _data['email2'] = next((x['email']['emailAddress'] for x in record.get('emails').get('emailInfo') if
                                x['email']['primaryInd'] is False), '')
    else:
        _data['email'] = ''
        _data['email2'] = ''

    if record.get('telephones'):
        _data['mobile'] = next((x['telephone']['phoneNumber'] for x in record.get('telephones').get('telephoneInfo') if
                                x['telephone']['phoneUseType'] == 'MOBILE'), '')
        _data['telephone'] = next(
            (x['telephone']['phoneNumber'] for x in record.get('telephones').get('telephoneInfo') if
             x['telephone']['phoneUseType'] == 'BUSINESS'), '')
    else:
        _data['mobile'] = ''
        _data['telephone'] = ''

    return _data


def _get_address_details(record):
    _address1 = ''
    _address2 = ''
    _address3 = ''
    _state = ''
    _town = ''
    _postCode = ''
    if record.get('addresses').get('addressInfo') and len(record.get('addresses').get('addressInfo')) > 0:
        _address1 = record.get('addresses').get('addressInfo')[0].get('address').get('addressLine')[0] if len(
            record.get('addresses').get('addressInfo')[0].get('address').get('addressLine')) >= 1 else ''
        _address2 = record.get('addresses').get('addressInfo')[0].get('address').get('addressLine')[1] if len(
            record.get('addresses').get('addressInfo')[0].get('address').get('addressLine')) >= 2 else ''
        _address3 = record.get('addresses').get('addressInfo')[0].get('address').get('addressLine')[2] if len(
            record.get('addresses').get('addressInfo')[0].get('address').get('addressLine')) >= 3 else ''
        _state = record.get('addresses').get('addressInfo')[0].get('state')
        _town = record.get('addresses').get('addressInfo')[0].get('cityName')
        _postCode = record.get('addresses').get('addressInfo')[0].get('postalCode')

    return {
        'addressLine1': _address1,
        'addressLine2': _address2,
        'addressLine3': _address3,
        'countryId': record.get('customer').get('citizenCountry').get('code') if record.get('customer') else '',
        'nationalityId': record.get('customer').get('citizenCountry').get('code') if record.get('customer') else '',
        'state': _state,
        'town': _town,
        'postCode': _postCode
    }


def _transform_guest_profile(record):
    idObj = _create_guest_id_obj(record)
    bday = record.get('birthDate')
    record = record.get('profileDetails')
    guest = GuestsModelV2(
        _id=idObj.get('profile'),
        idObj=idObj,
        profileType=record.get('profileType'),
        title='',
        firstName=record.get('customer').get('personName')[0].get('givenName') if record.get(
            'profileType') == 'Guest' else record.get('company').get('companyName'),
        lastName=record.get('customer').get('personName')[0].get('surname') if record.get(
            'profileType') == 'Guest' else '',
        datesAndDurations={
            'birthDate': bday,
            'anniversary': None
        },
        address=_get_address_details(record),
        contactInfo=_get_contact_details(record),
        privacyInfo={
            'emailOptOut': not record.get('privacyInfo').get('optInEmail'),
            'marketingOptOut': record.get('privacyInfo').get('optInMarketResearch'),
            'smsOptOut': not record.get('privacyInfo').get('optInSms'),
            'privacyOptIn': record.get('privacyInfo').get('infoFromThirdParty'),
            'phoneOptOut': not record.get('privacyInfo').get('optInPhone')
        },
        documents={
        },
        metaInfo={
            'uRLs': record.get('uRLs'),
            'notes': record.get('comments'),
            'languageSpokenId': record.get('customer').get('language') if record.get('customer') else '',
            'profileDeliveryMethods': record.get('profileDeliveryMethods'),
            'profileMemberships': record.get('profileMemberships'),
            'preferenceCollection': record.get('preferenceCollection'),
            'keywords': record.get('keywords'),
            'profileIndicators': record.get('profileIndicators'),
            'relationships': record.get('relationships'),
            'relationshipsSummary': record.get('relationshipsSummary'),
            'profileAccessType': record.get('profileAccessType'),
            'profileRestrictions': record.get('profileRestrictions'),
            'taxInfo': record.get('taxInfo'),
            'salesInfo': record.get('salesInfo'),
            'subscriptions': record.get('subscriptions'),
        },
        company=record.get('company'),
        registeredProperty=str(record.get('registeredProperty')),
        auraRecordUpdatedOn=datetime.now(),
    )
    return guest


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
            _guest_profile = _transform_guest_profile(self._extract_guest_profile(hotelId, item))
            self.mongoV2.save(_guest_profile)
            _guest_list.append(ReservationGuestShort(
                guest=_guest_profile.id,
                primary=item.get('primary'),
                birthDate=item.get('birthDate'),
                arrivalTransport=item.get('arrivalTransport'),
                departureTransport=item.get('departureTransport')
            ))
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
            record['idObj'] = self._get_reservation_id(record.get('reservationIdList'), record.get('agent'),
                                                       record.get('hotelId'), record.get('id'))
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

            # _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/calls'
            # data = self.retrieve_data(record.get('hotelId'), _url)
            # record['callHistory'] = data.get('callHistory') if data else None

            # _url = f'{self.token.hostName}/rsv/v0/hotels/{hotel_id}/reservations/{resv_id}/inventoryItems'
            # data = self.retrieve_data(record.get('hotelId'), _url)
            # record['inventoryItems'] = data.get('inventoryItems') if data else None

            _url = f'{self.token.hostName}/csh/v0/hotels/{hotel_id}/reservations/{resv_id}/folios?includeFolioHistory=true&fetchInstructions=Account&fetchInstructions=Payee&fetchInstructions=Totalbalance&fetchInstructions=Windowbalances&fetchInstructions=Payment&fetchInstructions=Postings&fetchInstructions=Transactioncodes&fetchInstructions=Reservation'
            data = self.retrieve_data(record.get('hotelId'), _url)
            record['folioInformation'] = data.get('reservationFolioInformation') if data else None

            # _url = f'{self.token.hostName}/csh/v0/hotels/{hotel_id}/transactions?reservationList={resv_id}&idContext=OPERA&type=Reservation&includeGenerates=true&includeTransactionsWithFolioNo=true&includeTransactionsWithManualPostingOnly=true'
            # data = self.retrieve_data(record.get('hotelId'), _url)
            # if data:
            #     del data['links']
            # record['transactions'] = data

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
        reservationV2 = ReservationModelV2(
            _id=str(record.get('id')),
            orgId=self.orgId,
            agent=record.get('agent'),
            idObj=_create_reservation_id_obj(record),
            datesAndDuration={
                'createdDate': record.get('createDateTime'),
                'confirmedDate': record.get('createDateTime'),
                'arrivalDate': record.get('roomStay').get('arrivalDate'),
                'departureDate': record.get('roomStay').get('departureDate'),
                'cancelledDate': record.get('cancellation')[0].get('cxlDate'),
                'expectedTimes': {
                    'arrival': record.get('roomStay').get('expectedTimes').get('reservationExpectedArrivalTime'),
                    'departure': record.get('roomStay').get('expectedTimes').get('reservationExpectedDepartureTime')
                },
                'originalTimeSpan': None,
                'lastModifyDateTime': record.get('lastModifyDateTime'),
                'createBusinessDate': record.get('createBusinessDate'),
                'createDateTime': record.get('createDateTime'),
                'eta': None,
                'event': None
            },
            status=_get_status(record.get('reservationStatus')),
            correspondence=None,
            metaInfo={
                'allowMobileCheckout': record.get('allowMobileCheckout'),
                'allowMobileViewFolio': record.get('allowMobileViewFolio'),
                'allowPreRegistration': record.get('allowPreRegistration'),
            },
            property={
                'hotelId': str(record.get('hotelId')),
                'hotelName': str(record.get('hotelId')),
                'roomId': str(record.get('folioInformation').get('reservationInfo').get('roomStay').get('roomId')),
                'roomName': str(record.get('folioInformation').get('reservationInfo').get('roomStay').get('roomId')),
                'categoryName': record.get('folioInformation').get('reservationInfo').get('roomStay').get('roomType'),
                'roomClass': record.get('folioInformation').get('reservationInfo').get('roomStay').get('roomClass'),
                'numberOfRooms': record.get('folioInformation').get('reservationInfo').get('roomStay').get(
                    'numberOfRooms'),
                'bedConfiguration': None
            },
            stayInfo={
                'longTerm': None,
                'businessSegmentId': None
            },
            reservationTypes={
                'type': 'Normal'
            },
            bookingInfo={
                'upgradeEligible': record.get('upgradeEligible'),
                'upgradeReason': None,
                'bookingMedium': record.get('roomStay').get('bookingMedium'),
                'bookingMediumDescription': record.get('roomStay').get('bookingMediumDescription'),
                'sourceOfSaleType': record.get('sourceOfSale').get('sourceType'),
                'sourceOfSaleCode': record.get('sourceOfSale').get('sourceCode'),
                'travelAgentId': record.get('folioInformation').get('reservationInfo').get('roomStay').get(
                    'bookingChannelCode'),
                'travelAgentName': record.get('folioInformation').get('reservationInfo').get('roomStay').get(
                    'bookingChannelCode'),
                'marketSegment': record.get('roomStay').get('roomRates')[0].get('marketCodeDescription'),
                'subMarketSegment': None,
                'notes': None,
            },
            financeInfo={
                'accountId': None,
                'rateTypeId': record.get('folioInformation').get('reservationInfo').get('roomStay').get('ratePlanCode'),
                'rateTypeName': record.get('folioInformation').get('reservationInfo').get('roomStay').get(
                    'ratePlanCode'),
                'totalPoints': record.get('roomStay').get('totalPoints').get('points'),
                'totalSpending': {
                    'amountBeforeTax': record.get('cashiering').get('revenuesAndBalances').get('totalRevenue').get(
                        'amount'),
                    'taxAmount': record.get('cashiering').get('revenuesAndBalances').get('totalPayment').get(
                        'amount') - record.get('cashiering').get('revenuesAndBalances').get('totalRevenue').get(
                        'amount') if (record.get('cashiering').get('revenuesAndBalances').get('totalPayment').get(
                        'amount') and record.get('cashiering').get('revenuesAndBalances').get('totalRevenue').get(
                        'amount')) else 0,
                    'totalRate': record.get('cashiering').get('revenuesAndBalances').get('totalPayment').get('amount')
                },
                'projectedTotalSpending': None,
                'paymentMethod': record.get('reservationPaymentMethods'),
                'other': None,
                'revenueBucketsInfo': None,
                'transactions': [],
                'revenue': {
                    'totalFixedCharge': {
                        'amount': record.get('cashiering').get('revenuesAndBalances').get('totalRevenue').get('amount')
                    },
                    'totalPayment': {
                        'amount': record.get('cashiering').get('revenuesAndBalances').get('totalPayment').get('amount')
                    },
                    'roomRevenue': {
                        'amount': record.get('cashiering').get('revenuesAndBalances').get('roomRevenue').get('amount')
                    },
                    'foodAndBevRevenue': {
                        'amount': record.get('cashiering').get('revenuesAndBalances').get('foodAndBevRevenue').get(
                            'amount')
                    },
                    'otherRevenue': {
                        'amount': 0
                    },
                    'totalRevenue': {
                        'amount': record.get('cashiering').get('revenuesAndBalances').get('totalRevenue').get('amount')
                    },
                    'balance': {
                        'amount': record.get('cashiering').get('revenuesAndBalances').get('balance').get('amount')
                    }
                },
                'deposit': {
                    'deposit': record.get('folioInformation').get('reservationInfo').get('roomStay').get(
                        'depositPayments').get('amount') if record.get('folioInformation').get('reservationInfo').get(
                        'roomStay').get('depositPayments') else 0,
                    'depositRequiredByDate': record.get('reservationPolicies').get('depositPolicies')[0].get(
                        'policy').get('deadline').get('absoluteDeadline') if len(
                        record.get('reservationPolicies').get('depositPolicies')) > 0 else None,
                    'secondDeposit': 0,
                    'secondDepositRequiredByDate': None,
                },
                'discount': [],
                'package': _get_package_info(record.get('reservationPackages')),
                'commission': {
                    'travelAgentCommissionPercentage': None
                }
            },
            daily_activity=_generate_day_to_day_entry(record),
            linkedReservation=[record.get('linkedReservation')],
            guestInfo=self._get_guest_info(record),
            eCertificates=record.get('eCertificates'),
            historyEvents=[],
            cancellation=_transform_cancellation_record(record.get('cancellation'),
                                                        record.get('reservationPolicies').get('cancellationPolicies')),
            housekeeping=[],
            comments=[],
            policies=record.get('reservationPolicies'),
            inventoryItems=record.get('inventoryItems'),
            preferences=[],
            requirement=[],
            rego_access=None,
            memberships=record.get('reservationMemberships'),
            packages=record.get('reservationPackages'),
            transfers=None,
            auraRecordUpdatedOn=datetime.now()
        )

        return reservationV2

    def _load_to_mongodb(self, record):

        try:
            logging.info(f'Adding reservation {record.id} to db {record.orgId}')
            self.mongo.get_collection(self.mongo.RESERVATION_COLLECTION).update_one({'_id': record.id},
                                                                                    {'$set': record.dict(
                                                                                        exclude={'token', 'id'})},
                                                                                    upsert=True)
        except Exception as e:
            logging.error(f'Error storing to respective {record.id} to db {record.orgId}')
            logging.error(e)

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
            del record['token']
            record = self._extract_reservation_details(record)
            record = self._transform_reservation(record)
            self.mongoV2.save(record)
            store_reservation_to_alvie(record)

    def __del__(self):
        logging.info(f'API calls made: {self._api_call_counter}')
        if self.mongo:
            self.mongo.close_connection()
        if self.mongoV2:
            self.mongoV2.close_connection()
