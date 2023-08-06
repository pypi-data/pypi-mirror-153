import unittest
import datetime
from gadgethiServerUtils.time_basics import *

class TimeTests(unittest.TestCase):
    """
    Testing Strategy:
    - serverTime
        - partition on mode: EPOCH, STRING, DATETIME_NOW
    
    - is_time_between
        - partition on check_time: None, or epoch time
        - partition on begin_time, end_time: begin < end, begin = end, begin > end

    - check_operation_hours
        - partition on opening_time, closing_time: open < close, open = close, open > close, XX

    - timeout
        - partition on timeout time: 0, 1, >1
        - partition on execution time: 0, 1, >1
        - partition on results: timedout, no timeout
    """

    # covers serverTime modes
    def test_servertime(self):
        self.assertTrue(isinstance(serverTime(), (int, float)), "server time defaults to number")

        self.assertTrue(isinstance(serverTime(TimeMode.STRING), str), "server time string format")

        self.assertTrue(isinstance(serverTime(TimeMode.DATETIME_NOW), datetime.datetime), "server time datetime format")

    # covers is_time_between
    def test_is_time_between(self):
        self.assertFalse(is_time_between(datetime.time(12, 10), datetime.time(10, 10), datetime.time(11, 10)), "check time between, begin > end")

        self.assertTrue(is_time_between(datetime.time(10, 10), datetime.time(10, 10), datetime.time(10, 10)), "check time between, begin = end")

        self.assertTrue(is_time_between(datetime.time(10, 10), datetime.time(19, 10), datetime.time(11, 10)), "check time between, begin < end")

    # covers check_operation_hours
    def test_check_operation_hours(self):
        args_dict = {
            "opening_time": "10:10",
            "closing_time": "12:10"
        }
        self.assertEqual(check_operation_hours(**args_dict), \
            datetime.datetime.now(tz=timez).time() >= datetime.time(10, 10) and datetime.datetime.now(tz=timez).time() <= datetime.time(12, 10))

        args_dict = {
            "opening_time": "XX",
            "closing_time": "XX"
        }
        self.assertFalse(check_operation_hours(**args_dict))

        args_dict = {
            "opening_time": "19:10",
            "closing_time": "08:10"
        }
        self.assertEqual(check_operation_hours(**args_dict), \
            datetime.datetime.now(tz=timez).time() >= datetime.time(19, 10) or datetime.datetime.now(tz=timez).time() <= datetime.time(8, 10))

        args_dict = {
            "opening_time": "10:10",
            "closing_time": "10:10"
        }
        self.assertEqual(check_operation_hours(**args_dict), \
            datetime.datetime.now(tz=timez).time() >= datetime.time(10, 10) and datetime.datetime.now(tz=timez).time() <= datetime.time(10, 10))

    # covers all timeout
    def test_timeout(self):

        @timeout(0)
        def test_sleep_0(n):
            time.sleep(n)
            return 'Done'

        @timeout(1)
        def test_sleep_1(n):
            time.sleep(n)
            return 'Done'

        @timeout(5)
        def test_sleep_5(n):
            time.sleep(n)
            return 'Done'

        with self.assertRaises(TimeoutError):
            test_sleep_0(1)

        with self.assertRaises(TimeoutError):
            test_sleep_1(2)

        self.assertEqual(test_sleep_5(0), "Done")
        self.assertEqual(test_sleep_1(0), "Done")
        self.assertEqual(test_sleep_5(1.2), "Done")
        