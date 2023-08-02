# from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
#
# def format_date(date):
#     return date.strftime('%d/%m/%Y')
#
# def abc():
#     today = datetime.now()
#     date_ranges = []
#
#     for months in [1, 2, 3]:
#         end_date = today - timedelta(days=1)
#         start_date = end_date - timedelta(days=months * 30 - 1)
#         date_ranges.append((format_date(start_date), format_date(end_date)))
#
#     print(date_ranges)
#
# abc()


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def format_date(date):
    return date.strftime('%d/%m/%Y')

def abc():
    today = datetime.now()
    # print(format_date(today))
    d30 = today - timedelta(days=30)
    # print(format_date(d30))
    d60 = today - timedelta(days=60)
    # print(format_date(d60))
    d90 = today - timedelta(days=90)
    # print(format_date(d90))

    date_ranges = [
        (d30, today),
        (d60, d30 - timedelta(days=1)),
        (d90, d60 - timedelta(days=1))
    ]

    for date_range in date_ranges:
        start_date, end_date = date_range
        print(format_date(start_date), '---', format_date(end_date))

abc()


### result expected:

# 02/07/2023 --- 01/08/2023
# 02/06/2023 --- 01/07/2023
# 03/05/2023 --- 01/06/2023