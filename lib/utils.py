import datetime
from datetime import timedelta
from mailgun import *

import pytz

from xlab.env_settings import *
from xlab.settings import TIME_ZONE

def get_down_sample_factor(count, max_allowed=1000, default_sample_rate=10):
    """
    For a given count, return the sample rate to be used so that the max. number of
    values does not exceed max_allowed. If a default_sample_rate is provided this
    function returns the same value if the condition is met.
    """
    if (count / default_sample_rate) < max_allowed: return default_sample_rate

    while((count / default_sample_rate) > max_allowed):
        default_sample_rate = default_sample_rate + 1

    return default_sample_rate

Mailgun.init(MAILGUN_API_KEY)
def send_email(sender, recipients, subject, message):
    MailgunMessage.send_txt(sender, recipients, subject, message)

def browser_is_supported(user_agent):
    response = True

    for ua in UNSUPPORTED_BROWSERS:
        if ua in user_agent:
            response = False
            break
            
    return response


def get_time_range_tuple(timezone, days=1):
    """
    This method returns a tuple of start and end times. The end time is the
    beginning of the current day and the start time is the specified number of
    days in the past. The time stamps are UTC time in the specified timezone.
    This is useful when we always want to pull out data from a midnight to
    midnight range in a user's given time zone and time is stored in UTC.

    Example: Making the call get_time_tuple("America/Los_Angeles", 1)
    on Jul 13, 2011 at 4:15 am would return (1310454000, 1310540400), i.e,
    (12 am Jul 12 2011, 12 am 13 Jul 2011) in the "America/Los_Angeles" timezone.
    """
    dt = datetime.datetime.now(pytz.timezone(timezone))
    dt_utc = dt.astimezone(pytz.utc)
    td = dt_utc - timedelta(days=days, hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    start_time = int(td.strftime("%s"))
    
    return (start_time, (start_time + days * 24 * 60 * 60))

def utc_datetime(datetime, timezone):
    """
    For a given datetime object and timezone, this
    method returns a datetime object for the corresponding UTC time.
    NOTE: This method assumes that the server is set to UTC.
    For example:
    >>> utc_strptime(datetime.datetime.strptime('07/13/2011 16:20', '%m/%d/%Y %H:%M'), "America/New_York")
    datetime.datetime(2011, 7, 13, 20, 20, tzinfo=<UTC>)
    """
    if datetime.tzinfo is None or datetime.tzinfo is pytz.utc:
        return datetime
    
    tz = pytz.timezone(timezone)
    return tz.localize(datetime).astimezone(pytz.utc)

def tz_strftime(timestamp, tz, pattern):
    return datetime.datetime.fromtimestamp(
            timestamp, pytz.timezone(tz)).strftime(pattern)

def str_to_timestamp(datetime_str, pattern, tz=TIME_ZONE):
    """
    This function accepts a datetime string, the pattern and a specified
    timezone and returns the corresponding unix timestamp with daylight savings
    time accounted for.
    """
    timezone = pytz.timezone(tz)
    dt = datetime.datetime.strptime(datetime_str, pattern)
    dt2 = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute,
        dt.second, dt.microsecond)
    return timezone.localize(dt2).strftime("%s")

def user_is_approver(user):
    """
    Checks if the user is allowed to approve trips
    """
    if user:
        return (user.is_staff or (user.groups.filter(name=APPROVER_GROUP_NAME).count() == 1))
    return False