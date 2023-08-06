import upswingutil as ul
from upswingutil.db import MongodbV2
from upswingutil.db.model import ReservationModel, Status


ul.MONGO_URI = 'mongodb://AdminUpSwingGlobal:Upswing098812Admin0165r@dev.db.upswing.global:27017/?authSource=admin&readPreference=primary&appname=Agent%20Oracle%20Dev&ssl=false'


if __name__ == '__main__':
    print('testing resv creation')
    orgId = 'OHIPB2'
    mongo = MongodbV2(orgId)
    resv = ReservationModel(_id="t2")
    resv.agent = 'test'
    resv.status = Status.CANCELLED
    mongo.save(resv)
    mongo.close_connection()
    print('completed')
