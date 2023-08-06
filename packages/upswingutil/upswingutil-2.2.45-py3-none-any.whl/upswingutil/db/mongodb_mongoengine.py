import logging
import ssl
import os
import mongoengine
from loguru import logger
import upswingutil as ul

__PII_FIELDS__ = ['guestGiven', 'guestSurname', 'mobile', 'passportId', 'email', 'email2']

mongoengine.connect(host='mongodb://ReadWrite:gbyate0ewA712Dkq823gswX9i1oP@dev.db.upswing.global:27017/?authSource=admin&readPreference=primary&appname=Aura&ssl=false')


class MongodbV2:
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
    DAILY_REPORTS_COLLECTION = 'daily_reports'

    def __init__(self, db_name):
        try:
            self.db_name = str(db_name)
            mongoengine.get_connection(db_name)
        except mongoengine.connection.ConnectionFailure as err:
            mongoengine.connect(db_name, host=os.getenv('MONGO_URI', ul.MONGO_URI), alias=db_name)
        except Exception as e:
            logger.error('Error while connecting to db')
            logger.error(type(e))

    def save(self, doc: mongoengine.DynamicDocument):
        logger.info(f'Data saved successfully to {self.db_name} : {doc.id}')
        doc.switch_db(self.db_name)
        doc.save()

    def close_connection(self):
        try:
            mongoengine.disconnect(self.db_name)
        except Exception as e:
            logger.error('Error while closing connection to db')
            logger.error(e)


if __name__ == '__main__':
    mongo = MongodbV2('11249')
    mongo.close_connection()
