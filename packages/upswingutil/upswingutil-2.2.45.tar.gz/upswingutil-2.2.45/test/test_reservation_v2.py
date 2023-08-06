import datetime
import logging
import unittest
import firebase_admin
from firebase_admin import credentials

import upswingutil as ul
from upswingutil.pms import rms, oracle
from upswingutil.resource import access_secret_version, setup_logging
import json


class TestReservationV2API(unittest.TestCase):
    ul.G_CLOUD_PROJECT = 'aura-staging-31cae'
    ul.ENCRYPTION_SECRET = "S1335HwpKYqEk9CM0I2hFX3oXa5T2oU86OXgMSW4s6U="
    ul.MONGO_URI = access_secret_version(ul.G_CLOUD_PROJECT, 'MONGOURI', '5')
    ul.LOG_LEVEL_VALUE = logging.DEBUG

    def test_adding_new_RMS_reservation(self):
        setup_logging()
        print('Initializing default firebase app')
        cred = json.loads(
            access_secret_version(ul.G_CLOUD_PROJECT, 'Firebase-Aura', '1'))
        cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(cred)

        print('Initializing alvie firebase app')
        cred = json.loads(
            access_secret_version(ul.G_CLOUD_PROJECT, 'Firebase-Alvie', '3'))
        cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(cred, name='alvie')

        resv = rms.ReservationSync('11281')
        resv_list = [204862]
        # resv_list = [187162]
        for _resv_id in resv_list:
            start_time = datetime.datetime.now()
            print(f'processing reservation : {_resv_id}')
            resv.process(_resv_id)
            print(f'processed reservation : {_resv_id}')
            end_time = datetime.datetime.now()
            print(f'total time to process : {end_time-start_time}')

    def test_adding_new_ORACLE_reservation(self):
        setup_logging()
        print('Initializing default firebase app')
        cred = json.loads(
            access_secret_version(ul.G_CLOUD_PROJECT, 'Firebase-Aura', '1'))
        cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(cred)

        print('Initializing alvie firebase app')
        cred = json.loads(
            access_secret_version(ul.G_CLOUD_PROJECT, 'Firebase-Alvie', '1'))
        cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(cred, name='alvie')

        resv = oracle.ReservationSync('OHIPSB')
        resv_list = [
            {
                'reservation': 17151,
                'hotelId': 'SAND01'
            },
            {
                'reservation': 16960,
                'hotelId': 'SAND01'
            },
            {
                'reservation': 17152,
                'hotelId': 'SAND01'
            },
            {
                'reservation': 17406,
                'hotelId': 'SAND01'
            },
            {
                'reservation': 17400,
                'hotelId': 'SAND01'
            },
            {
                'reservation': 16995,
                'hotelId': 'SAND01'
            },
            {
                'reservation': 17007,
                'hotelId': 'SAND01'
            },
        ]
        for _resv in resv_list:
            print(f'processing reservation : {_resv}')
            resv.process(_resv.get('reservation'), _resv.get('hotelId'))
            print(f'processed reservation : {_resv}')
