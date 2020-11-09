from datetime import datetime, timedelta
import calendar

# No year because I generally assume you at least know the year
formatter = "%d.%m"


def dates(start_year, start_month, start_day, end_year, end_month, end_day):
    start_date = int(datetime(start_year, start_month, start_day).timestamp() * 1000)
    end_date = int(datetime(end_year, end_month, end_day).timestamp() * 1000)

    if start_date > end_date:
        raise TypeError("Start can't be after end")
    else:
        return start_date, end_date


def split_time_for_threads(start: int, end: int, divider: float):
    split_stamps = [start]
    steps = (end - start) * (1 / divider)
    while round(start) < end:
        start = start+steps
        split_stamps.append(start)
    if split_stamps[len(split_stamps)-1] != end:
        split_stamps[len(split_stamps) - 1] = end
    return split_stamps

def range_of_week():
    current_date = datetime.utcnow()
    start_of_week = (current_date - timedelta(days=current_date.weekday()))
    end_of_week = (start_of_week + timedelta(days=7))

    return start_of_week, end_of_week


def range_of_month():
    current_date = datetime.utcnow()

    start_of_month = datetime.utcnow()
    start_of_month = start_of_month.replace(start_of_month.year, start_of_month.month, 1)
    end_of_month = start_of_month.replace(start_of_month.year, start_of_month.month,
                                          calendar.monthrange(current_date.year, current_date.month)[1])

    return start_of_month, end_of_month


def range_of_year():
    current_date = datetime.utcnow()
    start_of_year = datetime(current_date.year, 1, 1)

    return start_of_year, current_date


def create_timestamp(date: datetime):
    return int(datetime.timestamp(date))
