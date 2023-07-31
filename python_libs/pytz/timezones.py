from datetime import datetime

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
    print(f'Now date for Colombia: {naive_date.strftime(datetime_format)}')
    print(f'Now date for Colombia: {aware_date.strftime(datetime_format)}')


if __name__ == '__main__':
    # add_timezone_to_naive_date()
    using_datetime_now()
