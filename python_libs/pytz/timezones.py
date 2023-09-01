from datetime import datetime
from zoneinfo import ZoneInfo

import pytz


def add_timezone_to_naive_date():
    datetime_format = '%Y-%m-%d %H:%M:%S %Z%z'
    naive_date = datetime(2023, 3, 22, 13, 15, 15)
    aware_date = pytz.timezone('America/Panama').localize(naive_date)
    print(f'Naive date for Colombia: {naive_date.strftime(datetime_format)}')
    print(f'Aware date for Colombia: {aware_date.strftime(datetime_format)}')
    naive_timestamp = naive_date.timestamp()
    aware_timestamp = aware_date.timestamp()
    print(f'Naive timestamp: {int(naive_timestamp)}')
    print(f'Aware timestamp: {int(aware_timestamp)}')


def using_datetime_now():
    datetime_format = '%Y-%m-%d %H:%M:%S %Z%z'
    naive_date = datetime.now()
    timezone = pytz.timezone('America/Panama')
    aware_date = datetime.now(timezone)
    print(f'Now naive date for Colombia: {naive_date.strftime(datetime_format)}')
    print(f'Now aware date for Colombia: {aware_date.strftime(datetime_format)}')


def convert_to_utc():
    datetime_format = '%Y-%m-%d %H:%M:%S %Z%z'
    naive_date = datetime(2023, 3, 22, 13, 15, 15)
    pty_timezone = pytz.timezone('America/Panama')
    utc_timezone = pytz.utc
    pty_aware_date = pty_timezone.localize(naive_date, is_dst=None)
    # pty_aware_date = datetime.now(pty_timezone)
    # utc_date = pty_aware_date.astimezone(utc_timezone)
    # utc_date = utc_timezone.localize(pty_aware_date, is_dst=None)
    utc_date = pty_aware_date.astimezone(utc_timezone)
    print(f'Now UTC   date for Colombia: {utc_date.strftime(datetime_format)}')
    print(f'Now -0500 date for Colombia: {pty_aware_date.strftime(datetime_format)}')
    print('-' * 80)
    # Conclusions if the dates are the same but if different timezon representations the delta is 0
    delta = utc_date - pty_aware_date
    print(f'Delta: {delta}')
    print('-' * 80)
    # Conclusion: If the dates are the same but in differetne timezone representations the timestamp is the same
    print(f'UTC   timestamp for Colombia: {int(utc_date.timestamp())}')
    print(f'-0500 timestamp for Colombia: {int(pty_aware_date.timestamp())}')


def datetime_created_with_timezone():
    """
    Do not user pytz.timezone to create a datetime use ZoneInfo.
    """
    datetime_format = '%Y-%m-%d %H:%M:%S %Z%z'
    pty_timezone = pytz.timezone('America/Panama')
    pty_aware_date = datetime(2023, 3, 22, 13, 15, tzinfo=pty_timezone)
    pty_aware_date2 = datetime(2023, 3, 22, 13, 15, tzinfo=ZoneInfo('America/Panama'))

    print(f'Now -0500 date for Colombia: {pty_aware_date.strftime(datetime_format)}')
    print(f'ISO Format {pty_aware_date.isoformat()}')

    print(f'Now -0500 date for Colombia: {pty_aware_date2.strftime(datetime_format)}')
    print(f'ISO Format {pty_aware_date2.isoformat()}')


if __name__ == '__main__':
    # add_timezone_to_naive_date()
    # using_datetime_now()
    # convert_to_utc()

    datetime_created_with_timezone()
