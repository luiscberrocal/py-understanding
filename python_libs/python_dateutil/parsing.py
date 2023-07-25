from datetime import datetime

from dateutil.parser import parse


def parse_jira_date(date_str:str) -> datetime:
    dt = parse(date_str)
    return dt


if __name__ == '__main__':
    jira_date = ''