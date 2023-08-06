import unittest
import upswingutil as ul
from upswingutil.integrations import get_holiday_list


class TestHolidayAPI(unittest.TestCase):

    def test_calling_api(self):
        get_holiday_list()
