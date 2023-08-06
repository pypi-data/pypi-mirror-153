from enum import Enum
from .alvie import store_reservation_to_alvie


class PMS(str, Enum):
    ORACLE = 'ORACLE'
    RMS = 'RMS'
