from datetime import date, timedelta


def generate_trip_dates(start_date: date, end_date: date, allowed_isoweekdays, excluded_dates):
    trip_dates = []
    if end_date < start_date:
        return trip_dates

    current_date = start_date
    while current_date <= end_date:
        if current_date not in excluded_dates and current_date.isoweekday() in allowed_isoweekdays:
            trip_dates.append(current_date)
        current_date = current_date + timedelta(days=1)

    return trip_dates


def excluded_dates_from_iso_array(dates_iso):
    return map(date.fromisoformat, dates_iso)

