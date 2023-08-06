import dateutil.parser
import datetime
import pytz
import tzlocal
import time

class Dates:

    @staticmethod
    def diff_months(d1: datetime, d2: datetime) -> int:
        return (d1.year - d2.year) * 12 + d1.month - d2.month

    @staticmethod
    def get_current_timezone() -> str:
        return tzlocal.get_localzone().zone

    @staticmethod
    def parse_datetime(datetime: datetime) -> datetime:
        return dateutil.parser.parse(datetime).replace(tzinfo=None)

    @staticmethod
    def now(type: str=None) -> datetime:
        date = datetime.datetime.now()

        if type == 'DATE':
            return date.date()
        elif type == 'TIME':
            return date.time()
        else:
            return date

    @staticmethod
    def subtract(date: datetime, value: int, unit_of_measure: str) -> datetime:
        if unit_of_measure == 'SECONDS':
            delta = datetime.timedelta(seconds=value)
        elif unit_of_measure == 'MINUTES':
            delta = datetime.timedelta(minutes=value)
        elif unit_of_measure == 'HOURS':
            delta = datetime.timedelta(hours=value)
        elif unit_of_measure == 'DAYS':
            delta = datetime.timedelta(days=value)

        return date - delta

    @staticmethod
    def change_timezone(datetime: datetime, from_timezone_code: str='Europe/Rome', to_timezone_code: str='US/Pacific') -> datetime:
        # create both timezone objects
        old_timezone = pytz.timezone(from_timezone_code)
        new_timezone = pytz.timezone(to_timezone_code)

        return old_timezone.localize(datetime).astimezone(new_timezone)

    @staticmethod
    def get_timezone() -> str:
        return time.tzname

    @staticmethod
    def difference(datetime1: datetime, datetime2: datetime, measure: str) -> float:
        if measure == 'SECONDS':
            return (datetime2 - datetime1).total_seconds()
        elif measure == 'MINUTES':
            return (datetime2 - datetime1).total_seconds() / 60
        elif measure == 'HOURS':
            return (datetime2 - datetime1).total_seconds() / 3600
        elif measure == 'DAYS':
            return (datetime2 - datetime1).total_seconds() / 86400