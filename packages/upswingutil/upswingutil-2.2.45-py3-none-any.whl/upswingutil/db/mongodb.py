import ssl
import os
from pymongo import MongoClient
from loguru import logger
import upswingutil as ul

__PII_FIELDS__ = ['guestGiven', 'guestSurname', 'mobile', 'passportId', 'email', 'email2']


class Mongodb:
    RESOURCE_COLLECTION = 'resource'
    AREAS_COLLECTION = "areas"
    GUEST_COLLECTION = "guests"
    PROPERTY_COLLECTION = "properties"
    RESERVATION_COLLECTION = "reservations"
    TRANSACTION_COLLECTION = "transactions"
    AREA_REPORTS_BY_DAY_COLLECTION = "area_report_by_day"
    COUNTRIES_COLLECTION = 'countries'
    ORG_CONFIG_COLLECTION = 'org_config'
    COUNTERS_COLLECTION = 'counters'
    EVENTS_COLLECTION = 'events'
    CANCELLATION_POLICIES = 'cancellationPolicies'
    DAILY_REPORTS_COLLECTION = 'daily_report'
    OFFERS_COLLECTION = 'offers'
    OFFERS_CAMPAIGN_COLLECTION = 'offers_campaigns'
    OFFERS_FEEDBACK_COLLECTION = 'offers_feedback'
    OTA_CHANNEL_COLLECTION = 'ota_channel'
    IOT_ROOM_MAPPING = 'iot_room_mapping'
    INTEGRATION_PROPERTY = 'integration_property'
    INTEGRATION_ORG = 'integration_org'
    OFFERS_TARGETGROUP_COLLECTION = 'offers_targetgroups'
    APP_USERS_MANAGEMENT_COLLECTION = 'app_user_management'
    AURA_SUBSCRIPTIONS_COLLECTION = "aura_subscriptions"
    UPSWING_INTEGRATIONS = 'integrations'


    def __init__(self, db_name):
        try:
            self.db_name = str(db_name)
            self.client = MongoClient(
                os.getenv('MONGO_URI', ul.MONGO_URI),
                # ssl_cert_reqs=ssl.CERT_NONE
            )
            self.db = self.client[str(db_name)]
        except Exception as e:
            logger.error('Error while connecting to db')
            logger.error(e)


    def get_collection(self, name):
        try:
            return self.db[name]
        except Exception as e:
            logger.error('Error while connecting to db')
            logger.error(e)


    def create_view(self, view_name, view_on, pipeline):
        return self.db.command({
            "create": view_name,
            "viewOn": view_on,
            "pipeline": pipeline
        })


    def execute_pipeline(self, name: str, pipeline: list):
        try:
            return list(self.db.get_collection(name).aggregate(pipeline))
        except Exception as e:
            logger.error('Error while executing pipeline')
            logger.error(e)


    def close_connection(self):
        try:
            if self.client:
                self.client.close()
        except Exception as e:
            logger.error('Error while closing connection to db')
            logger.error(e)


if __name__ == '__main__':
    mongo = Mongodb('11249')
    val = mongo.get_collection(mongo.GUEST_COLLECTION)
    print(val)
    mongo.close_connection()
