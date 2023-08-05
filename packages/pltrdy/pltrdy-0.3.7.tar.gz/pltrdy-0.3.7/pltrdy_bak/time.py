import datetime
import pytz

EPOCH = "01/01/1970"
TZ_PARIS = "Europe/Paris"
DATE_FORMAT_DMY = "%d/%m/%Y"
DATE_FORMAT_ISO = "%Y-%m-%d %H:%M:%S"


def now(timezone=TZ_PARIS):
    timezone = pytz.timezone(timezone)
    now_tz = timezone.localize(datetime.datetime.now())
    return now_tz


def str_to_date(date_str, date_format=DATE_FORMAT_DMY, timezone=TZ_PARIS):
    timezone = pytz.timezone(timezone)
    date = datetime.datetime.strptime(date_str, date_format)
    datetz = timezone.localize(date)
    return datetz


def date_to_str(date, date_format=DATE_FORMAT_ISO):
    s = datetime.datetime.strftime(date, DATE_FORMAT_ISO)
    return s


def str_to_timestamp(date_str, date_format=DATE_FORMAT_DMY, timezone=TZ_PARIS):
    datetz = str_to_date(date_str, date_format, timezone)
    return datetz.timestamp()


def timestamp_to_str(t, date_format=DATE_FORMAT_ISO):
    d = datetime.datetime.fromtimestamp(t)
    s = date_to_str(date, date_format)
    return s
