import urllib
import requests
from datetime import datetime, timedelta
from upswingutil.db import Firestore
from upswingutil.resource import decrypt
from upswingutil.schema import Token
from loguru import logger


def validate_key(expiryDate):
    """
    Validated whether the token is still valid or not
    :param expiryDate:
    :return:
    """
    try:
        if expiryDate is None:
            return False
        return datetime.fromisoformat(expiryDate) > (datetime.now() + timedelta(minutes=5))
    except Exception as e:
        logger.error('Error while validating key')
        logger.error(e)
        return False


def get_key(org_id: str, refresh_toke=None) -> Token:
    """
    This method generates auth token for provided org_id, in case of refreshing token,
    provide refresh_token, to generate new token using it.

    :param org_id:
    :param refresh_toke:
    :return: instance of Token
    """
    try:
        db = Firestore()
        pms = db.get_collection(db.org_collection).document(org_id).get().to_dict().get('pms')
        url = f"{pms.get('hostName')}/oauth/v1/tokens"
        auth_base64 = pms.get('client').decode("utf-8")
        app_key = decrypt(pms.get('appKey'))
        if refresh_toke:
            payload = f'refresh_token={refresh_toke}&grant_type=refresh_token'
            logger.debug('Refreshing token key')
        else:
            logger.debug('Generating NEW token key')
            payload = urllib.parse.urlencode({
                'username': decrypt(pms.get('username')),
                'password': decrypt(pms.get('password')),
                'grant_type': 'password'
            })
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'x-app-key': app_key,
            'Authorization': f'Basic {auth_base64}'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            logger.error('POST /authToken {}'.format(response.status_code))
            logger.error(response.__str__())
            logger.error(response.reason)
        else:
            data = dict(response.json())
            return Token(
                key=data.get('access_token'),
                refreshKey=data.get('refresh_token'),
                validity=str(datetime.now() + timedelta(seconds=int(data.get('expires_in')))),
                hostName=pms.get('hostName'),
                appKey=app_key
            )
    except Exception as e:
        logger.error('Error generating token key oracle')
        logger.error(e)


if __name__ == '__main__':
    orgId = "SAND01"
    token, valid, refresh = get_key(orgId)
    print('with username password')
    print('token', token)
    print('valid', valid)
    print('refresh', refresh)
    print('with refresh token')
    token, valid, refresh = get_key(orgId, refresh)
    print('token', token)
    print('valid', valid)
    print('refresh', refresh)
