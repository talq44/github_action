import sys
from datetime import datetime, timedelta, timezone

major = 2
count = 0

def korea_time():
    korea_time = datetime.utcnow() + timedelta(hours=9)
    return korea_time

def current_year():
    current_year = korea_time().year
    return current_year % 100

def current_week():
    current_week = korea_time().isocalendar()[1]
    return current_week

def is_january():
    current_month = korea_time().month
    return  current_month == 1

def is_december():
    current_month = korea_time().month
    return  current_month == 12

def is_firstweek():
    return current_week() == 1

def is_weekOfDecember():
    return current_week() > 48

def current_version():
    if is_january() and is_weekOfDecember():
        return f"{major}.{current_year()}.01{count}"
    elif is_december() and is_firstweek():
        return f"{major}.{current_year() + 1}.{current_week():02d}{count}"

    return f"{major}.{current_year()}.{current_week():02d}{count}"

def versioncode_lastcount_plus_one(version):
    versions = version.split(".")
    if len(versions) != 3:
        return version

    major = versions[0]
    year = versions[1]
    week_and_count = int(versions[2]) + 1

    return f"{major}.{year}.{week_and_count:03d}"


def new_version(version):

    if version is None:
        return ""

    new_version = current_version()
    if version >= current_version():
        new_version = versioncode_lastcount_plus_one(version)

    return (f"{new_version}")

# 명령행 인수에서 값을 받음
if len(sys.argv) > 1:
    value = sys.argv[1]
    version = new_version(value)
    print(version)
else:
    version = current_version()
    print(version)