from datetime import datetime

from dateutil.parser import parse


def parse_jira_date(date_str: str) -> datetime:
    dt = parse(date_str)
    return dt


def format_date(value: str):
    date_format = '%d/%b/%Y %I:%M %p'
    try:
        dt = datetime.strptime(value, date_format)
        return dt
    except Exception as e:
        print(f'{value}')
        print(f'{e}')
        raise e


if __name__ == '__main__':
    jira_date_str = '25/Jul/23 2:23 PM'
    jira_date = parse_jira_date(jira_date_str)
    print(jira_date)

    # This will raise an error because the hour need to be zero padded.
    jira_date = format_date(jira_date_str)