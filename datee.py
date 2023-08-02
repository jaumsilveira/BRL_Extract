from datetime import datetime, timedelta

def format_date(date):
    return date.strftime('%d/%m/%Y')

def abc():
    today = datetime.now()

    date_ranges = [
        (timedelta(days=30 * i), timedelta(days=30 * (i - 1)) + timedelta(days=1) if i > 1 else None) for i in range(1, 13)
    ]

    for start_date, end_date in date_ranges:
        print(format_date(today - start_date), '---', format_date(today - end_date) if end_date else format_date(today))

abc()
