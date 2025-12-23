from datetime import datetime, timedelta

def get_date_range(period: str):
    """
    Returns start_date, end_date based on period.
    Allowed: today, yesterday, last_7_days, last_30_days, this_month, last_month.
    """

    today = datetime.today().date()

    if period == "today":
        return today, today

    elif period == "yesterday":
        y = today - timedelta(days=1)
        return y, y

    elif period == "last_7_days":
        return today - timedelta(days=7), today

    elif period == "last_30_days":
        return today - timedelta(days=30), today

    elif period == "this_month":
        start = today.replace(day=1)
        return start, today

    elif period == "last_month":
        first_day_this_month = today.replace(day=1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        return first_day_last_month, last_day_last_month

    else:
        raise ValueError("Invalid period. Allowed: today, yesterday, last_7_days, last_30_days, this_month, last_month.")
