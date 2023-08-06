import datetime
import time
import logging
import re
import os
from enum import Enum

# For timeout function
# ------------------------------
import concurrent.futures as futures

# timezone_str should be a integer number range from -24 to 24, 
# this is the offset from UTC. TODO: CAVEAT: Be careful of the daylight saving
timezone_str = os.environ.get('SERVER_TIMEZONE', '8') #Defaults to UTC +8
timez = datetime.timezone(datetime.timedelta(hours=int(timezone_str)))

class TimeMode(Enum):
    EPOCH = 1
    STRING = 2
    DATETIME_NOW = 3

def serverTime(mode=TimeMode.EPOCH):
    """
    This defines the current server time.
    Make sure all time related function take 
    on this time. 
    * Input:
        mode: the mode of the serverTime representation. If
            not specified -> epoch time will be returned
    * Returns a datetime object
    """
    server_time = datetime.datetime.now(tz=timez)
    
    if mode == TimeMode.EPOCH:
        return server_time.timestamp()
    elif mode == TimeMode.STRING:
        return server_time.strftime("%m-%d-%Y-%H-%M-%S")
    elif mode == TimeMode.DATETIME_NOW:
        return server_time


def is_time_between(begin_time, end_time, check_time=None):
    """
    This is the function to check whether the check time is between
    begin_time and end_time. Input types are datetime objects. 
    # If check time is not given, default to current UTC time
    """
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time <= end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def check_operation_hours(**kwargs):
    """
    Given opening_time, closing_time. 
    return True if it's is within operation hours. 
    return False if not.

    - Input
        * opening_time, closing_time: 08:00, 10:00, XX
    """
    # HH:MM regex
    hhmmregex = "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
    opening_time, closing_time = kwargs["opening_time"], kwargs["closing_time"]

    if not bool(re.search(hhmmregex, opening_time)) or (not bool(re.search(hhmmregex, closing_time))):
        return False

    opening_hour, opening_minute = int(opening_time[:2]), int(opening_time[3:])
    closing_hour, closing_minute = int(closing_time[:2]), int(closing_time[3:])
    logging.info("[VerifyOperationHour] opening_hour, closing_hour = "+ str(opening_hour) + str(closing_hour))

    start_time = datetime.time(opening_hour,opening_minute)
    end_time = datetime.time(closing_hour,closing_minute)
    current_time = serverTime(TimeMode.DATETIME_NOW).time()

    return is_time_between(start_time, end_time, current_time)


def timeout(timelimit):
    """
    The timeout decorator for functions to raise
    Timeout error if certain timelimit is reached. 
    This is from 
    https://stackoverflow.com/questions/56356125/setting-timeout-limit-on-windows-with-python-3-7
    which is compatible for Windows and UNIX system unlike the "signal" approach
    """
    def decorator(func):
        def decorated(*args, **kwargs):
            with futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(func, *args, **kwargs)
                try:
                    result = future.result(timelimit)
                except futures.TimeoutError:
                    logging.error('[TIMEOUT] Timeout '+str(timelimit)+" sec triggered...")
                    raise TimeoutError from None
                else:
                    logging.info(result)
                executor._threads.clear()
                futures.thread._threads_queues.clear()
                return result
        return decorated
    return decorator


