# from datetime import datetime
# from upswingutil.resource import get_model_from_cloud_storage
# from upswingutil.pms.rms import NAME, get_key, validate_key
# from upswingutil.db import Mongodb, Firestore
# from upswingutil.schema import Token
# import upswingutil as ul
# import requests
# import logging
# import asyncio
# from concurrent.futures import ThreadPoolExecutor
#
#
# def _get_geo_region(nationalID: int):
#     result = 'unknown'
#     try:
#         mongo = Mongodb('upswing')
#         region = mongo.get_collection('countries').find_one({"_id": nationalID}, {"region": 1})
#         mongo.close_connection()
#         result = region if region else 'unknown'
#     except Exception as e:
#         logging.error(f'Error getting geo region of nation {nationalID}')
#         logging.error(e)
#     finally:
#         return result
#
#
# @DeprecationWarning
# class ReservationSync:
#
#     def __init__(self, orgId: str, g_cloud_token=None):
#         self.orgId = orgId
#         self.mongo = Mongodb(orgId)
#         self.token: Token = get_key(self.orgId)
#         self.g_cloud_token = g_cloud_token
#         self.__urgent_booking_criteria__ = 5 * 86400
#         self.__stay_duration_criteria__ = 10 * 86400
#         self.__booking_category_levels__ = ['bronze', 'silver', 'gold', 'platinum']
#
#     def _get_booking_type(self, arrival_date: str, created_date: str):
#         result = 'unknown'
#         try:
#             delta = datetime.fromisoformat(arrival_date) - datetime.fromisoformat(created_date)
#             delta = delta.days * 86400 + delta.seconds
#             result = 'Urgent Booking' if delta < self.__urgent_booking_criteria__ else 'Pre Planned'
#         except Exception as e:
#             logging.error('Error while calculating booking type')
#             logging.error(e)
#         finally:
#             return result
#
#     def _get_duration_type(self, departure_date: str, arrival_date: str):
#         result = 'unknown'
#         try:
#             stay_d = datetime.fromisoformat(departure_date) - datetime.fromisoformat(arrival_date)
#             delta = stay_d.days * 86400 + stay_d.seconds
#             result = 'Short Stay' if delta < self.__stay_duration_criteria__ else 'Long Stay'
#         except Exception as e:
#             logging.error('Error calculating stay duration type')
#             logging.error(e)
#         finally:
#             return result
#
#     def _get_booking_level(self, orgId, clientId, departure_date: str, arrival_date: str, spend, booking_type):
#         result = 'unknown'
#         try:
#             stay_d = datetime.fromisoformat(departure_date) - datetime.fromisoformat(arrival_date)
#             booking_type_id = 1 if booking_type == 'Urgent Booking' else 0
#             model = get_model_from_cloud_storage(
#                 str(orgId),
#                 f'booking_categorization_{clientId}.pkl',
#                 token=self.g_cloud_token
#             )
#             prediction = model.predict([[stay_d.days, spend, booking_type_id]])
#             level = prediction[0] if len(prediction) > 0 else None
#             result = self.__booking_category_levels__[level] if level else 'unknown'
#         except Exception as e:
#             logging.error('Error calculating booking_level of reservation')
#             logging.error(e)
#         finally:
#             return result
#
#     def _retrieve_data(self, id, name, url):
#         result = None
#         try:
#             logging.debug(f'Extracting {name} for reservation: {id}')
#             header = {
#                 'Content-Type': 'application/json',
#                 'authtoken': self.token.key
#             }
#             response = requests.request("GET", url, headers=header)
#             if response.status_code == 200:
#                 result = response.json()
#             else:
#                 logging.error(f'Error getting {name} for reservation {id} due to status code {response.status_code}')
#                 logging.error(url.format(id))
#         except Exception as e:
#             logging.error(f' {name} failed due to {e}')
#         finally:
#             return result
#
#     def extract_reservation_details(self, record):
#         feature_list = [
#             {
#                 'name': 'holds',
#                 'url': 'holds'
#             },
#             {
#                 'name': 'guests',
#                 'url': 'guests'
#             },
#             {
#                 'name': 'billTo',
#                 'url': 'billTo'
#             },
#             {
#                 'name': 'transfers',
#                 'url': 'transfers'
#             },
#             {
#                 'name': 'auditTrail',
#                 'url': 'auditTrail'
#             },
#             {
#                 'name': 'daily_rates',
#                 'url': 'dailyRates'
#             },
#             {
#                 'name': 'rego_access',
#                 'url': 'regoAccess'
#             },
#             {
#                 'name': 'requirement',
#                 'url': 'requirements'
#             },
#             {
#                 'name': 'housekeeping',
#                 'url': 'housekeeping'
#             },
#             {
#                 'name': 'daily_revenue',
#                 'url': 'dailyRevenue'
#             },
#             {
#                 'name': 'add_ons',
#                 'url': 'reservationAddOn'
#             },
#             {
#                 'name': 'correspondence',
#                 'url': 'correspondence'
#             },
#             {
#                 'name': 'financial_info_actual',
#                 'url': 'actualAccount'
#             },
#             {
#                 'name': 'bedConfiguration',
#                 'url': 'bedConfiguration'
#             },
#         ]
#         try:
#             logging.info(f"Extracting reservation {record.get('id')} additional details.")
#
#             for item in feature_list:
#                 _url = f"{self.token.hostName}/reservations/{record.get('id')}/{item.get('url')}"
#                 record[item.get('name')] = self._retrieve_data(record.get("id"), item.get("name"), _url)
#             return record
#         except Exception as e:
#             logging.error(f'Error retrieving addition reservation details for {record.get("id")}')
#             logging.error(e)
#
#     def transform_reservation(self, record):
#         try:
#             logging.info(f'Transforming reservation {record.get("id")}')
#             record['booking_type'] = self._get_booking_type(record['arrivalDate'], record['createdDate'])
#             record['duration_type'] = self._get_duration_type(record['departureDate'], record['arrivalDate'])
#             record['globalId'] = f"{record.get('agent')}-{record.get('orgId')}-{record.get('clientId')}-{record.get('id')}"
#             record['booking_level'] = self._get_booking_level(
#                 record.get('orgId'),
#                 record['clientId'], record['departureDate'],
#                 record['arrivalDate'], record['financial_info_actual']['totalRate'],
#                 record['booking_type']
#             )
#             return record
#         except Exception as e:
#             logging.error(f"Exception while transforming reservation {record.get('id')}")
#             logging.error(e)
#
#     def transform_guest(self, record):
#         try:
#             logging.info(f'Transforming guests of reservation {record.get("id")}')
#             for guest in record.get('guests'):
#                 guest['_id'] = guest.get('id')
#                 del guest['id']
#                 guest['geoRegion'] = _get_geo_region(guest.get('nationalityId'))
#             return record
#         except Exception as e:
#             logging.error(f'Error while transforming guest for reservation {record.get("id")}')
#             logging.error(e)
#
#     def _add_reservation_to_alvie(self, record):
#         firestore_db = Firestore(app='alvie')
#         user_email_list = [item["email"] for item in record.get('guests')]
#         resv_info = {
#             "_id": record.get("id"),
#             "agent": record.get("agent"),
#             "orgId": record.get("orgId"),
#             "areaId": record.get("areaId"),
#             "arrivalDate": record.get("arrivalDate"),
#             "departureDate": record.get("departureDate"),
#             "propertyId": record.get("propertyId"),
#             "propertyName": record.get("propertyName"),
#             "status": record.get("status"),
#             "travelAgentId": record.get("travelAgentId"),
#             "travelAgentName": record.get("travelAgentName")
#         }
#         logging.debug(f"Final reservation id : {record.get('id')}")
#         for email in user_email_list:
#             docs = firestore_db.get_collection('users').where("email", "==", email).stream()
#             for doc in docs:
#                 logging.info("loading reservation to alvie")
#                 firestore_db.get_collection(f'users/{doc.id}/reservations') \
#                     .document(str(record.get("id"))) \
#                     .set(resv_info, merge=True)
#                 logging.debug(f"added to {doc.id}")
#
#     def extract_reservation(self, record):
#         reservationId = record.get("reservation")
#         logging.info(f'Extracting reservation: {reservationId}')
#
#         header = {
#             'Content-Type': 'application/json',
#             'authtoken': self.token.key
#         }
#         url = f"{self.token.hostName}/reservations/{reservationId}?modelType=full"
#         response = requests.request("GET", url, headers=header)
#         if response.status_code == 200:
#             try:
#                 response_json = dict(response.json())
#                 response_json['orgId'] = self.orgId
#                 response_json['agent'] = record.get('agent')
#                 property_info = self.mongo.get_collection(self.mongo.PROPERTY_COLLECTION).find_one(
#                     {"areas.id": response_json.get('areaId')},
#                     {'id': 1, 'name': 1,
#                      'clientId': 1}
#                 )
#                 response_json['clientId'] = property_info.get('clientId') if property_info else 0
#                 response_json['propertyId'] = property_info.get('_id') if property_info else 0
#                 response_json['propertyName'] = property_info.get('name') if property_info else 'Unknown'
#                 return response_json
#             except Exception as err:
#                 logging.error(f'{record} load failed due to {err}')
#         else:
#             logging.error(f"RMS returned status code {response.status_code} "
#                           f"for reservation {reservationId} ")
#             raise Exception('Reservation not found / unable to retrieve')
#
#     def _load_to_mongodb(self, record):
#         _id = record.get("id")
#         orgId = record.get("orgId")
#         record.update({'lastUpdate': str(datetime.now())})
#         try:
#             logging.info(f'Adding reservation {_id} to db {orgId}')
#             self.mongo.get_collection(self.mongo.RESERVATION_COLLECTION).update_one({'_id': _id},
#                                                                           {'$set': record}, upsert=True)
#         except Exception as e:
#             logging.error(f'Error storing to respective {_id} to db {orgId}')
#             logging.error(e)
#
#     def process(self, reservationId):
#         record = {
#             'orgId': self.orgId,
#             'agent': NAME,
#             'reservation': reservationId
#         }
#
#         if not validate_key(self.token.validity):
#             logging.info('Refreshing RMS token as it is about to expire')
#             self.token = get_key(self.orgId)
#
#         record = self.extract_reservation(record)
#         record = self.extract_reservation_details(record)
#         record = self.transform_reservation(record)
#         record = self.transform_guest(record)
#         self._load_to_mongodb(record)
#         self._add_reservation_to_alvie(record)
#
#     def __del__(self):
#         if self.mongo:
#             self.mongo.close_connection()
#
#
# if __name__ == '__main__':
#     ul.G_CLOUD_PROJECT = 'aura-staging-31cae'
#     ul.ENCRYPTION_SECRET = "S1335HwpKYqEk9CM0I2hFX3oXa5T2oU86OXgMSW4s6U="
#     ul.FIREBASE = '/Users/harsh/upswing/github/agent-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-' \
#                   '7c135838e9.json'
#     ul.MONGO_URI = "mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSo" \
#                    "urce=admin&readPreference=primary&appname=Agent%20RMS%20Dev&ssl=false"
#     import firebase_admin
#     cred = firebase_admin.credentials.Certificate(ul.FIREBASE)
#     firebase = firebase_admin.initialize_app(cred)
#     resv = ReservationSync('11249')
#     resv.process(23560)
#     resv.process(23590)
