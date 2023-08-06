from upswingutil.resource import decrypt, http_retry
from loguru import logger
from upswingutil.schema import Token
from datetime import datetime, timedelta
from upswingutil.db import Firestore


def validate_key(expiryDate):
    try:
        if expiryDate is None:
            return False
        return datetime.fromisoformat(expiryDate) > (datetime.now() + timedelta(minutes=30))
    except Exception as e:
        logger.error('Error while validating key')
        logger.error(e)
        return False


def get_key(org_id):
    db = Firestore()
    client = db.get_collection(db.org_collection).document(org_id).get().to_dict()
    url = client["pms"]["url"]
    body = {
        "agentId": client["pms"]["agentId"],
        "agentPassword": decrypt(client["pms"]["agentPassword"]),
        "clientId": client["pms"]["clientId"],
        "clientPassword": decrypt(client["pms"]["clientPassword"]),
        "useTrainingDatabase": client["pms"]["useTrainingDatabase"],
        "moduleType": client["pms"]["moduleType"]
    }
    try:
        http = http_retry()
        resp = http.post(url + '/authToken', json=body)
        if resp.status_code != 200:
            logger.error('POST /authToken {}'.format(resp.status_code))
            logger.error(resp.__str__())
            logger.error(resp.reason)
        else:
            return Token(
                key=resp.json()['token'],
                validity=resp.json()['expiryDate'],
                hostName=url
            )
    except Exception as e:
        logger.error('Exception generating auth token for RMS')
        logger.error(e)
