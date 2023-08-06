import unittest
from upswingutil.ml import Classification_Cancellation_NoShow_Others
import upswingutil as ul
from upswingutil.pms import PMS

ul.ENCRYPTION_SECRET = "S1335HwpKYqEk9CM0I2hFX3oXa5T2oU86OXgMSW4s6U="
ul.MONGO_URI = "mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSource=admin&readPreference=primary&appname=Agent%20Oracle%20Dev&ssl=false"
ul.G_CLOUD_PROJECT = "aura-staging-31cae"
ul.FIREBASE = "/Users/harsh/upswing/github/api-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-7c135838e9.json"
ul.LOG_LEVEL_VALUE = 'DEBUG'

class TestClassification_Cancellation_NoShow_Others(unittest.TestCase):

    def test_creating_model_oracle(self):
        """
        Training model for ORACLE
        """
        orgId = 'OHIPSB'
        classifier_cancel_noshow_others = Classification_Cancellation_NoShow_Others(PMS.ORACLE, orgId)
        # classifier_cancel_noshow_others.preprocess()
        # classifier_cancel_noshow_others.train()

    def test_creating_model_rms(self):
        """
        Training model for RMS
        """
        orgId = '11249'
        classifier_cancel_noshow_others = Classification_Cancellation_NoShow_Others(PMS.RMS, orgId)
        classifier_cancel_noshow_others.preprocess()
        classifier_cancel_noshow_others.train()

    def test_predict_rms(self):
        '''
        Creating the Model and Make Predictions on the Trained Model
        '''
        orgId = '11249'
        classifier_cancel_noshow_others = Classification_Cancellation_NoShow_Others(PMS.RMS, orgId)
        ## Features to Predict on:
        clientId= 0                             ## Int
        rateTypeName='Old system rate'          ## String
        Class= 'None'                           ## String
        durationOfStay= 11.0                    ## Float
        bookingWindowDays= 52.0                 ## Float
        guestCount= 1                           ## Int

        ## For Checking the results
        result = "Cancelled"

        final, overall = classifier_cancel_noshow_others.predict(clientId, rateTypeName, Class, durationOfStay, bookingWindowDays, guestCount)
        assert result==final


    def test_predict_oracle(self):
        pass


if __name__ == '__main__':
    unittest.main()