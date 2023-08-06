import datetime
import logging

from upswingutil.db import Mongodb
from upswingutil.schema import GuestUserProfileModel, ResponseDict

def create_and_update_app_user_profile(orgId: str, user_data: GuestUserProfileModel):
    response = ResponseDict(status = False, message = "", data = {})
    try:
        mongo = Mongodb(orgId)
        _user_exists = mongo.get_collection(mongo.APP_USERS_MANAGEMENT_COLLECTION)\
            .find_one({'firstName': user_data.firstName,'lastName': user_data.lastName, 'email': user_data.email, 'mobile': user_data.mobile})
        if _user_exists == None:
            data = user_data.dict()
            data['_id'] = f"{user_data.firstName}-{user_data.lastName}-{user_data.email}-{user_data.mobile}"
            data['createdAt'] = datetime.datetime.utcnow()
            _usr_inserted = mongo.get_collection(mongo.APP_USERS_MANAGEMENT_COLLECTION).insert_one(data)
            if _usr_inserted.acknowledged:
                response.data = {'inserted_id': _usr_inserted.inserted_id}
                response.status = True
            else:
                response.message = "Unable to create the user profile"
        else:
            _updated_user = mongo.get_collection(mongo.APP_USERS_MANAGEMENT_COLLECTION).\
                find_one_and_update({'firstName': user_data.firstName,'lastName': user_data.lastName, 'email': user_data.email, 'mobile': user_data.mobile},
                                    {'$addToSet': {'bookings': user_data.bookings[0].dict()}}, upsert=True)
            response.status = True
            response.message = 'Added Reservation to existing Users'
    except Exception as e:
        logging.error("Error occured in creating profile in AURA User Management")
        logging.error(e)
        response.message = f"Exception Occured {e.__str__()}"
    finally:
        return response