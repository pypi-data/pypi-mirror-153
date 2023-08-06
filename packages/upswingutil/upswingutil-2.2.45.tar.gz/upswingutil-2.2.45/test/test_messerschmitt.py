import json
import logging
import unittest

import firebase_admin
from firebase_admin import credentials

import upswingutil as ul
from upswingutil.integrations.messerschmitt import get_key
from upswingutil.resource import access_secret_version
from upswingutil.schema import Token

ul.G_CLOUD_PROJECT = "aura-staging-31cae"
ul.ENCRYPTION_SECRET = access_secret_version(ul.G_CLOUD_PROJECT, 'ENCRYPT_SECRET_KEY', '1')


try:
    firebase_admin.get_app()
except Exception as e:
    logging.info('Initializing default firebase app')
    cred = json.loads(access_secret_version(ul.G_CLOUD_PROJECT, 'Firebase-Alvie', '1'))
    cred = credentials.Certificate(cred)
    firebase = firebase_admin.initialize_app(cred)


try:
    firebase_admin.get_app('alvie')
except Exception as e:
    logging.info('Initializing default firebase app')
    cred = json.loads(access_secret_version(ul.G_CLOUD_PROJECT, 'Firebase-Alvie', '1'))
    cred = credentials.Certificate(cred)
    firebase = firebase_admin.initialize_app(name='alvie', credential=cred)


class TestMesserschmitt(unittest.TestCase):

    def test_get_key(self):
        orgId = '11281'
        token: Token = get_key(orgId)
        print(token.json())

    def test_get_key_with_app(self):
        orgId = '11281'
        token: Token = get_key(orgId, 'alvie')
        print(token.json())

