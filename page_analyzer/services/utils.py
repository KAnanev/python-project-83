from datetime import datetime


def get_date_now():
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')
