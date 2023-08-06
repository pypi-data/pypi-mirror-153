from enum import Enum

from .email import create_dataflow_job_for_sending_emails, trigger_reservation_email, build_template, TriggerReservationEmailModel


class CHANNEL(str, Enum):
    EMAIL = 'email'
    WHATSAPP = 'whatsapp'
