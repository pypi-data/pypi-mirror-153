import unittest
from upswingutil.ml import ReservationCountForecast
import upswingutil as ul
from upswingutil.pms.oracle import NAME as ORACLE
from upswingutil.pms.rms import NAME as RMS

ul.ENCRYPTION_SECRET = "S1335HwpKYqEk9CM0I2hFX3oXa5T2oU86OXgMSW4s6U="
ul.MONGO_URI = "mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSource=admin&readPreference=primary&appname=Agent%20Oracle%20Dev&ssl=false"
ul.G_CLOUD_PROJECT = "aura-staging-31cae"
ul.FIREBASE = "/Users/harsh/upswing/github/api-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-7c135838e9.json"
ul.LOG_LEVEL_VALUE = 'DEBUG'


class TestReservationCountForecasting(unittest.TestCase):

    def test_creating_model_oracle(self):
        """
        Training model for ORACLE
        """
        orgId = 'OHIPSB'
        propertyId = 'SAND01'
        resvCountForecast = ReservationCountForecast(ORACLE, orgId, propertyId)
        resvCountForecast.train()

    def test_creating_model_rms(self):
        """
        Training model for RMS
        """
        orgId = '11249'
        propertyId = '11264'
        resvCountForecast = ReservationCountForecast(RMS, orgId, propertyId)
        resvCountForecast.train()

    def test_predict_rms(self):
        orgId = '11249'
        propertyId = '11264'
        rcf = ReservationCountForecast(RMS, orgId, propertyId)
        startDate = '2021-01-01'
        endDate = '2021-02-01'
        key, val = rcf.predict(startDate, endDate)
        avg = (sum(val) / len(val))
        self.assertTrue(len(key) > 0)
        self.assertTrue(len(val) > 0)
        self.assertTrue(avg >= 0)
        print(f'Avg predicted value for {startDate} till {endDate} is {avg}')


if __name__ == '__main__':
    unittest.main()
