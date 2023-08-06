import datetime
import logging
from typing import List, Optional

from googleapiclient.discovery import build
from pydantic import BaseModel

import upswingutil as ul
from upswingutil.db import Mongodb, Firestore


class ParameterModel(BaseModel):
    orgId: str
    toList: str
    smtpHost: str
    smtpPort: str
    fromEmail: str  # //use .decode('utf-8')
    password: str  # //use .decode('utf-8')
    subject: str
    template: str
    source: str
    campaignId: str
    reservationId: str


class TriggerReservationEmailModel(BaseModel):
    orgId: str
    hotelId: str
    hotelName: str
    reservationId: str
    firstName: str
    lastName: str = ''
    guestEmail: str
    arrivalDate: str
    departureDate: str


def build_template(template: str, v_name: List, r_name: List):
    i = 0
    for v in v_name:
        template = template.replace(v, r_name[i])
        i = i + 1
    return template


def create_dataflow_job_for_sending_emails(jobname: str, parameters: ParameterModel):
    dataflow = build('dataflow', 'v1b3')
    request = dataflow.projects().locations().templates().launch(
        projectId=ul.G_CLOUD_PROJECT,
        location='asia-south1',
        gcsPath="gs://dataflow-content/Communication/EmailTrigger/templates/email_trigger",
        body={
            'jobName': jobname,
            'parameters': parameters.dict()
        }
    )
    response = request.execute()
    return response


def trigger_reservation_email(data: TriggerReservationEmailModel):
    sent_time = datetime.datetime.utcnow()
    mongo = Mongodb(data.orgId)
    _smtp_record = mongo.get_collection(mongo.INTEGRATION_PROPERTY).find_one({"_id": f"{data.hotelId}-welcome-email", "hotelId": data.hotelId})
    logo = Firestore('alvie').get_ref_document(f'Organizations', data.orgId).to_dict()['logo']
    if _smtp_record == None:
        logging.error(f"Welcome Email not configured and SMTP Records are none")
    elif _smtp_record['allow_welcome_email']:
        _smtp_record['template'] = build_template(_smtp_record['template'],
                                                  ["{logo}","{hotelName}", "{reservationId}", "{firstName}", "{lastName}",
                                                   "{arrivalDate}", "{departureDate}"],
                                                  [logo,data.hotelName, data.reservationId, data.firstName, data.lastName,
                                                   data.arrivalDate, data.departureDate])
        parameters = ParameterModel(
            orgId=data.orgId,
            toList=data.guestEmail,
            smtpHost=_smtp_record['smtp_host'],
            smtpPort=_smtp_record['smtp_port'],
            fromEmail=f"{_smtp_record['emailId'].decode('utf-8')}",
            password=f"{_smtp_record['password'].decode('utf-8')}",
            subject=f"Welcome {data.firstName} to {data.hotelName}",
            template=_smtp_record['template'],
            source='reservation',
            campaignId='',
            reservationId=data.reservationId
        )

        res = create_dataflow_job_for_sending_emails(
            jobname=f"{data.orgId}-{data.hotelId}-WelcomeEmail-{data.reservationId}-{sent_time}", parameters=parameters)
        if 'job' in res:
            logging.info(f"Successfully Created the Welcome Email Job: {data.guestEmail}")
            mongo.close_connection()
            return True
        else:
            mongo.close_connection()
            return False
    else:
        logging.info(f"Welcome Email disabled for {data.orgId} : {data.hotelId}")